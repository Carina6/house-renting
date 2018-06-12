from datetime import datetime
from elasticsearch import Elasticsearch

# 连接elasticsearch,默认是9200
es = Elasticsearch()

# 创建索引，索引的名字是my-index,如果已经存在了，就返回个400，
# 这个索引可以现在创建，也可以在后面插入数据的时候再临时创建
es.indices.create(index='my-index')


# 插入数据,(这里省略插入其他两条数据，后面用)
es.index(index="my-index", doc_type="test-type", id=1, body={"any": "data01", "timestamp": datetime.now()})
# 也可以，在插入数据的时候再创建索引test-index
es.index(index="test-index", doc_type="test-type", id=42, body={"any": "data", "timestamp": datetime.now()})

# 查询数据，两种get and search
# get获取
res = es.get(index="my-index", doc_type='test-type', id='1')
print(res)

# # search获取
res = es.search(index="my-index", body={"query": {"match_all": {}}})
print(res)

res = es.search(index="test-index", body={'query': {'match': {'any': 'data'}}})  # 获取any=data的所有值
print(res)

# delete
# 删除指定id的记录
res = es.delete(index='my-index', doc_type='test-type', id='1')

# 删除指定index
es.delete_by_query(index="test-index", body={"query": {"match_all": {}}})
