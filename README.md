# Assistant API 相关概念

1. 一个Assistant相当于一个Agent。
2. 一个Thread相当于一个用户。
3. Run powers the execution of an Assistant on a Thread。
4. 每个Agent有各自的专长，一个Agent最多10~15个Function，过多导致性能急剧下降。

# Assistant API 与 Commer100 Bot集成

1. 先走意图识别，没有命中走Agent，RAG作为Agent的其中一个Function（可以同时被调用）。
2. RAG默认兜底（兜住非Function calling的全部用户问题），不可调用GPT自身能力作答。
3. 当用户问题唯一调用RAG时，可以返回Comm100定义格式。

# Assistant API持久化

1. Assistant API相关的对象（Threads, messages, runs, Files）数据存储在一个安全的、由Microsoft管理的存储帐户中，存储暂不收费。
2. 这些数据将在您通过API或仪表板删除后30天从我们的服务器中删除，未通过API或仪表板删除的对象将无限期保留。
3. 只要ID（Assistant ID, Threads ID, messages ID, runs ID, Files ID）在，数据就在，可以随时pull them up，与应用程序启停无关。
4. Code Intercepter收费0.03$ / session，File Search暂不收费。

# 测试用例

1. 商品详情
2. 订单详情（ROUND1: I would like to inquire about the details of my order. ROUND2: 789456123, please.）
3. 是否有货
    1. TODO 缺货推荐
4. 商品推荐
    1. 给出推荐理由
    2. TODO 语义检索
5. 转人工
6. RAG
7. 测试意图跳转
8. 测试必填字段

# 启动方式

1. 执行config.py，获取Assistant ID
2. uvicorn main:app --host 0.0.0.0
