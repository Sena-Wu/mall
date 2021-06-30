# flask_sqlalchemy数据库交互

以此段代码为例

```python
db = flask_sqlalchemy.SQLAlchemy()
wwq = Account(**{'account_name': 'wwq', 'addr': 'unknown', 'cell_phone': 'unknown', 'head_url': 'default.jpg', 'sex': 0, 'birthday': '2021-6-29', 'money': '99999999.99', 'create_time': '2021-06-29 20:31:28', 'update_time': '2021-06-29 20:31:28'})
db.session.add(wwq)
db.session.commit()
```

## session.add的作用

调用 `add()` 函数会添加对象。它会发出一个 INSERT 语句给数据库，但是由于事务仍然没有提交，您不会立即得到返回的 ID 。

调用 `add()`后并不会将对象写入数据库，即使在add之后数据库发生了其他的事务，依然不会写入数据库，故。。。该事务并没有被隐式的触发commit，又或者。。。**(未完待续。。。)**

**具体参考**<a href="#SQLAlchemy.Session.add()">SQLAlchemy.Session.add()</a> 

只有当调用`commit()`后对象写入数据库

参考资料：

http://www.pythondoc.com/flask-sqlalchemy/queries.html

https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html

## session.commit的作用

```python
session.commit()
```

提交事务。。。写数据库，没有这一步骤则无法修改数据库



# SQLAlchemy数据库交互

## Session.add()

```python
import sqlalchemy
from sqlalchemy import text
from sqlalchemy.orm import Session

engine = sqlalchemy.create_engine('mysql+pymysql://root:971211@127.0.0.1:3306/mall?charset=utf8')
session = Session(engine)

session.add(wwq) # 将wwq对象添加至Session中，并将wwq的状态设置为pending
session.new #查看
session.flush() #与数据库交互
session.execute(text("select * from account_tb where account_name='wwq'")).first()
session.commit()
```

在SQLAlchemy.Session中add的作用是将wwq对象添加至Session中，**并将wwq的状态设置为pending**。

**The opposite of ``add()`` is ``expunge()``.**

## Session.new

调用`Session.new`来查看pending状态的对象

```shell
>>> wwq
<Account (transient 2051868205320)>
>>> session.new
IdentitySet([<Account (transient 2051868205320)>])
```

## Session.flush()

Session.flush()与database交互，**并将对象wwq设置为persistent状态**：

```python
session.flush() # 将sql语句发送到mysql数据库
session.execute(text("select * from account_tb where account_name='wwq'")).first()
#(2237169, 'wwq', 'default.jpg', 'unknown', 'unknown', 0, datetime.date(2021, 6, 29), Decimal('99999999.99'), datetime.datetime(2021, 6, 29, 20, 31, 28), datetime.datetime(2021, 6, 29, 20, 31, 28))
wwq.id
#2237169
```

可以看出，经过flush后，已经能在database中查询到刚刚插入的数据，wwq对象的id属性也被检索赋值

flush()产生如下SQL语句与database交互：

```mysql
BEGIN (implicit)
INSERT INTO account_tb (account_name, ...) VALUES (?, ?)  #省略
[...] ('wwq', ...)
```

- **注意！！！！SQL语句中没有commit**
- **经过flush(),之后并没有实际的改写数据库，因为该事务并没有发生提交，或者回滚、关闭等操作，所以需要session.commit()来最终提交事务，写数据库**
- ~~在没有commit之前添加的数据被别的事务中的命令所读取也就是发生了读未提交，读未提交是指可以读到其它事务未提交的数据，由于其实事务未提交，很有可能会回滚操作，此时如果读取了未提交的事务，并且也使用了读到的数据，就会出现脏数据的问题，即脏读；~~

**若在此时，新建一个session，又插入一条数据，效果如下：**

```python
session1 = Session(engine)
wwj = Account(**{'account_name': 'wwj', 'addr': 'unknown', 'cell_phone': 'unknown', 'head_url': 'default.jpg', 'sex': 0, 'birthday': '2021-6-29', 'money': '99999999.99', 'create_time': '2021-06-30 02:31:28', 'update_time': '2021-06-30 02:31:28'})
session1.add(wwj)
session1.flush()

#session1读session1.flush的数据
session1.execute(text("select * from account_tb where account_name='wwj'")).first()
#(2237170, 'wwj', 'default.jpg', 'unknown', 'unknown', 0, datetime.date(2021, 6, 29), Decimal('99999999.99'), datetime.datetime(2021, 6, 30, 2, 31, 28), datetime.datetime(2021, 6, 30, 2, 31, 28))

#session1读session.flush的数据
session1.execute(text("select * from account_tb where account_name='wwq'")).all()
#[]

#session读session.flush的数据
session.execute(text("select * from account_tb where account_name='wwq'")).first()
#(2237169, 'wwq', 'default.jpg', 'unknown', 'unknown', 0, datetime.date(2021, 6, 29), Decimal('99999999.99'), datetime.datetime(2021, 6, 29, 20, 31, 28), datetime.datetime(2021, 6, 29, 20, 31, 28))

```

```shell
>>> wwq.id
2237169
>>> wwj.id
2237170
```

- 未commit之前，该事务内的数据不会被其他事务读取
- primary key编号接续之前INSERT语句所占用的编号

**session.flush()可省略**

```python
xixi = Account(**{'account_name': 'xixi', 'addr': 'unknown', 'cell_phone': 'unknown', 'head_url': 'default.jpg', 'sex': 0, 'birthday': '2021-6-29', 'money': '0', 'create_time': '2021-06-29 20:36:28', 'update_time': '2021-06-29 20:36:28'})
session.add(xixi)
session.flush()
session.commit()
#效果一致
dida = Account(**{'account_name': 'dida', 'addr': 'unknown', 'cell_phone': 'unknown', 'head_url': 'default.jpg', 'sex': 0, 'birthday': '2021-6-29', 'money': '0', 'create_time': '2021-06-29 20:37:28', 'update_time': '2021-06-29 20:37:28'})
session.add(dida)
session.commit()'0', 'create_time': '2021-06-29 20:31:28', 'update_time': '2021-06-29 20:31:28'})
```

## Session.commit

```python
session.commit() # Flush pending changes and commit the current transaction.
```

提交事务。。。写数据库，没有这一步骤则无法修改数据库

**存在多个事务的提交效果：**都提交的效果就很明显了。。。不展示

- session1提交，session尚未提交:

  ![image-20210630120436228](C:\Users\user\AppData\Roaming\Typora\typora-user-images\image-20210630120436228.png)

- 紧接着，session回滚：

  ![image-20210630121227510](C:\Users\user\AppData\Roaming\Typora\typora-user-images\image-20210630121227510.png)

  ```shell
  >>> session.rollback()
  >>> session.execute(text("select * from account_tb where account_name='wwq'")).all()
  []
  >>> session.execute(text("select * from account_tb where account_name='wwj'")).first()
  (2237170, 'wwj', 'default.jpg', 'unknown', 'unknown', 0, datetime.date(2021, 6, 29), Decimal('99999999.99'), datetime.datetime(2021, 6, 30, 2, 31, 28), datetime.datetime(2021, 6, 30, 2, 31, 28))
  ```

参考资料：

https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html