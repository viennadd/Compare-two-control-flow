#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/InstrTypes.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"

#include "rapidjson/document.h"

#include <iostream>
#include <queue>
#include <string>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <set>

using namespace llvm;
using namespace rapidjson;

namespace {
    struct TraversalPass : public FunctionPass
    {
        static char ID;

        TraversalPass() : FunctionPass(ID)
        { }

        virtual bool runOnFunction(Function &F)
        {
            // outs() << "CFG of " << F.getName() << " \n";

            Document json;

            // initial: {"start": "", "adjacency": []}
            json.Parse("{\"start\":\"\", \"function\":\"\", \"adjacency\": {} }");

            auto &start = json["start"];
            auto &function = json["function"];

            start.SetString(addressToString(&F.getEntryBlock()).c_str(), json.GetAllocator());
            function.SetString(F.getName().str().c_str(), json.GetAllocator());

            // BFS
            std::queue<BasicBlock *> q;
            std::set<BasicBlock *> visited_blocks;
            q.push(&F.getEntryBlock());
            while (!q.empty()) {
                // keep current basic block information
                auto currentBasicBlock = q.front();
                auto currentAdjacencyArray = rapidjson::Value(kArrayType);
                visited_blocks.insert(currentBasicBlock);
                // to do

                const auto pTerInst = currentBasicBlock->getTerminator();
                for (auto idx = 0; idx < pTerInst->getNumSuccessors(); ++idx) {
                    auto pSuccessor = pTerInst->getSuccessor(idx);
                    // keep edges
                    rapidjson::Value strSuccessor(kStringType);
                    strSuccessor.SetString(addressToString(pSuccessor).c_str(), json.GetAllocator());
                    currentAdjacencyArray.PushBack(strSuccessor, json.GetAllocator());
                    // to do

                    if (!exist(visited_blocks, pSuccessor))
                    {
                        visited_blocks.insert(pSuccessor);
                        q.push(pSuccessor);
                    }
                }

                addConnections(json, currentBasicBlock, currentAdjacencyArray);
                q.pop();
            }

            writeOut(std::cout, json);
            return false;
        }

        const bool exist(std::set<BasicBlock *> &visited_blocks, BasicBlock *p)
        {
            return visited_blocks.find(p) != visited_blocks.end();
        }

        void addConnections(Document &document, BasicBlock *pBasicBlock, rapidjson::Value &adjacency_array)
        {
            // add list: {"start": "", "adjacency": [{object_key:the_adjacency_array}, {}, {}] }
            rapidjson::Value &adjacency = document["adjacency"];
            rapidjson::Value object(kObjectType);

            rapidjson::Value adjacency_array_key(kStringType);
            adjacency_array_key.SetString(addressToString(pBasicBlock).c_str(), document.GetAllocator());
            
            adjacency.AddMember(adjacency_array_key, adjacency_array, document.GetAllocator());
            // object.AddMember(adjacency_array_key, adjacency_array, document.GetAllocator());
            // adjacency.PushBack(object, document.GetAllocator());
        }


        /*
         * map memory address to number
         *  - use number as ID of graph node
         * */
        std::string addressToString(void *pBB)
        {
            typedef std::pair<void *, int> pair;
            static std::map<void *, int> dict;
            static int max = 0;

            auto it = dict.find(pBB);

            if (it == dict.end()) {
                max++;
                dict.insert(pair(pBB, max));
                return std::to_string(max);
            } else {
                return std::to_string(it->second);
            }

        }

        void writeOut(std::ostream &out, Document &document)
        {
            StringBuffer buffer;
            Writer<StringBuffer> writer(buffer);
            document.Accept(writer);
            out << buffer.GetString() << std::endl;
        }

    };
}

char TraversalPass::ID = 0;

// Automatically enable the pass.
// http://adriansampson.net/blog/clangpass.html
static void registerTraversalPass(const PassManagerBuilder &,
                                  legacy::PassManagerBase &PM)
{
    PM.add(new TraversalPass());
}

static RegisterStandardPasses
        RegisterMyPass(PassManagerBuilder::EP_EarlyAsPossible,
                       registerTraversalPass);
