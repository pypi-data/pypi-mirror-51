#Datastore Client

Project TCT图像与信息存储数据库 Datastore python版Client

##示例
```python

if __name__ == "__main__":
    #test code
    #this test code shows that:
    #   crate a lot of raw datas
    #   upload them to datastore
    #   gather them togher to create a dataset name 'L-in-H'
    #   and query them out in tow style
    log.getLogger().setLevel(log.INFO)

    #DataStore Client, next coming: DataStore Command Line Tools
    client = Client(
        graphql_entrance = 'http://127.0.0.1:8080',
        minio_entrance = '127.0.0.1:9001',
        graphql_path="/v1/graphql/",
        minio_secure=False,
        download_path='./test_data'
    )
    

    for i in range(20):
        with open('./test_data/test{}.txt'.format(i), 'w+') as f:
            import random
            f.write(str('hi'))

    raws = client.raw.create('./test_data/', metadata={
        'bucket': 'raws', #the name of the bucket
        'source': 'tell me more detail where this object come from!',
        'class_tree': {
            'big_image': 'HSIL',
            'cell': 'LSIL',
            'instance': 'independent'
            },
        'hi':'this is a test, you can add any key you want',
        'but': 'every resources has a prototype keys that you must contains'
        }
    )

    err, dataset = client.dataset.create(name='L-in-H', metadata={
        "note": 'this dataset contains all the LSIL cell from HSIL big image'
        })

    err, dataset_with_raws = client.dataset.add_raws(
        dataset=dataset,
        resources=raws
        )

    err, raws = client.raw.query("""
        {
            dataset_id: {
                _eq: 1
            }
        }
        """)

    err, res = client.queryer.query(
        """
        {
          data_raw(where: {metadata: {_contains: {class_tree: {cell: "LSIL"}}}, tag: {_eq: "latest"}}, distinct_on: id) {
            id
            metadata
            tag
            version
            url
            name
          }
        }
        """
        )
    raws = res['data']['data_raw']
    print(client.downloader.download(raws))

    for i in range(20):
        os.remove('test_data/test{}.txt'.format(i))


```
##Package Document

使用python函数 help(object)查看文档

##Datastore API Reference

请参阅在线文档