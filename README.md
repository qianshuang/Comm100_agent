1. 一个Assistant相当于一个Agent
2. 一个Thread相当于一个用户
3. Run powers the execution of an Assistant on a Thread
4. 每个Agent有各自的专长，一个Agent最多10~15个Function，过多导致性能急剧下降
5. 先走意图识别，没有命中走Agent，RAG作为Agent的其中一个Function（可以同时被调用）
