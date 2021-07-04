

# SQLAlchemy数据库交互

参考资料：

https://www.osgeo.cn/sqlalchemy/index.html 中

https://docs.sqlalchemy.org/en/14/index.html 英

以此段代码为例

```python
import sqlalchemy
from sqlalchemy import text
from sqlalchemy.orm import Session
from .model import Account

wwq = Account(**{'account_name': 'wwq', 'addr': 'unknown', 'cell_phone': 'unknown', 'head_url': 'default.jpg', 'sex': 0, 'birthday': '2021-6-29', 'money': '99999999.99', 'create_time': '2021-06-29 20:31:28', 'update_time': '2021-06-29 20:31:28'})

engine = sqlalchemy.create_engine('mysql+pymysql://root:971211@127.0.0.1:3306/mall?charset=utf8')
session = Session(engine)

session.add(wwq) # 将wwq对象添加至Session中，并将wwq的状态设置为pending
session.new #查看pending状态对象集
session.flush() #与数据库交互
session.execute(text("select * from account_tb where account_name='wwq'")).first()
session.commit()
```

## Session.add()

在SQLAlchemy.Session中add的作用是将wwq对象添加至Session中由session管理，**并将wwq的<a href="#对象状态">状态</a>设置为pending**。

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

### 以add()后的flush为例

Session.flush()与database交互，**写数据库**(快照)，**并将对象wwq设置为persistent状态**：

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

### flush过程

flush是指对对象的挂起更改做出所有决定，以INSERT、UPDATE和DELETE语句的形式发送到数据库。

把new、dirty、delete集合中对象加入session上下文中、并生成一系列对应的SQL命令与数据库交互

参考：

https://www.osgeo.cn/sqlalchemy/orm/session_events.html#persistence-events 中

https://docs.sqlalchemy.org/en/14/orm/session_events.html#persistence-events 英

**session.flush()可省略**，因为commit()会默认先调用flush()，在向数据库发出查询语句之前也就自动调用flush()

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

- 提交事务。。。没有这一步骤，在MySQL**默认**的**可重复读的隔离级别**下，因为事务相互隔离，其他事务是无法查询到该未提交事务内部的更改(增、删、改)后的结果。**注！！！：一个事务是否能够读取其他事务的更改与数据库的隔离级别相关**。

- 如果**没有显式调用session.commit()**提交事务，程序便直接退出或者调用了session.close(),那么SQLAlchemy默认**会回滚之前的操作**。在只有select操作时可以不需要commit！

- 可以将Session设置为**autocommit模式，但是不推荐！！！！**因为在此模式下任何一条数据库操作作为一个单独的事务并自动提交到数据库。导致任何操作都不能回滚。

  ```python
  #添加数据
  session.add(wwq) #事务1，已被自动提交至数据库
  #欲撤回添加
  session.rollback() #事务2，无法对事务1进行回滚，撤销失败
  ```

**存在多个事务的提交效果：**都提交的效果就很明显了。。。不展示

- session1提交，session尚未提交:

  ![image-20210630120436228](./sqlalchemy/image-20210630120436228.png)

- 紧接着，session回滚：

  ![image-20210630121227510](./sqlalchemy/image-20210630121227510.png)

  ```shell
  >>> session.rollback()
  >>> session.execute(text("select * from account_tb where account_name='wwq'")).all()
  []
  >>> session.execute(text("select * from account_tb where account_name='wwj'")).first()
  (2237170, 'wwj', 'default.jpg', 'unknown', 'unknown', 0, datetime.date(2021, 6, 29), Decimal('99999999.99'), datetime.datetime(2021, 6, 30, 2, 31, 28), datetime.datetime(2021, 6, 30, 2, 31, 28))
  ```
  

参考资料：

https://www.osgeo.cn/sqlalchemy/orm/session_basics.html 中

https://docs.sqlalchemy.org/en/14/orm/session_basics.html 英

https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html 英

## Session

参考：

https://docs.sqlalchemy.org/en/14/glossary.html# sqlalchemy中的术语解释

https://juejin.cn/post/6844904164141580302

每当程序中发生了修改(增加、更新、删除)，都会产生一个更改事件，**无论什么时候查询数据或者提交事务**，session都会首先自动调用flush把所有pending等<a href="#对象状态">状态</a>的数据更改到数据库内存当中去。也就是说add()之后不需要flush或commit，通过query也能在数据库查询到添加的数据。到这就是[unit of work](https://www.osgeo.cn/sqlalchemy/glossary.html#term-unit-of-work)模式，即系统自动跟踪对象修改，并且定期的把这些pending等状态的修改更新到数据库。

**session维护了4个对象：**new=IdentitySet([])、delete=IdentitySet([])、dirty=IdentitySet([<Account 2237165>])、identity_map = <sqlalchemy.orm.identity.WeakInstanceDict object at 0x0000019CD8112CC8>

**new**: session.add(obj)把对象加入new集合中，new中包含了pending状态的对象

**delete**: session.delete(obj)把对象加入delete集合中，delete中包含了delete状态的对象

**dirty**: 对象发生更改后会被自动加到dirty集合中，并在下一次的flush被更新到数据库，dirty中包含了persistent状态并且被程序修改过的对象

**identity_map**: python对象及其数据库标识(主键)之间的映射。A mapping between Python objects and their database identities. The identity map is a collection that’s associated with an ORM Session object, and maintains a single instance of every database object keyed to its identity. 把当前Session上下文中从数据库查询结果集的每一行记录都映射为一个Python对象保存到Identity Map中，Map的key就是行的主键。**对数据库中的一行数据而言，无论发生多少次的更改和查询，只要是在同一个session下，任意一次对他查询/更新返回的都是同一个对象。**(每次query查询都要从数据库中取数据，而不是直接从**identity_map**中获取。)

## select/query

数据查询：其他查询方法不一一举例

```python
wwq = session.query(Account).filter_by(account_name='wwq').first()
#wwq: <Account 2237171>
type(wwq) #<class 'app.account.models.Account'>

wwq = session.query(Account).filter(Account.account_name=='wwq').first()
#wwq: <Account 2237171>
type(wwq) #<class 'app.account.models.Account'>

wwq = session.query(Account.account_name, Account.addr).first() 
#wwq: ('boss', '南大')
type(wwq) #<class 'sqlalchemy.engine.row.Row'>  

session.execute(text("select * from account_tb where account_name='wwq'")).first()
#wwq: (2237171, 'wwq', ... ,datetime.datetime(2021, 6, 29, 20, 31, 28))
type(wwq) #<class 'sqlalchemy.engine.row.Row'>  
```

<class 'app.account.models.Account'> 以属性方式直接查看、更改属性值 wwq.account_name = 'wwj'

<class 'sqlalchemy.engine.row.Row'> 不能修改，以查看字典key-value的方式查看 wwq['account_name']

2.0版本：

```python
from sqlalchemy import select
stmt = select(Account).where(Account.account_name == 'wwq')
wwq = session.execute(stmt).first()
type(wwq) # <class 'sqlalchemy.engine.row.Row'>
```

select操作是可以不需要commit的，因为他并没有对数据库做出任何的更改数据的操作

## Session.update()

更新数据：

```python
wwq.account_name = 'wwj' #直接修改对象属性
# 或
wwj = session.query(Account).filter_by(account_name='wwq').\
update({'account_name':'wwj'}).first()
# wwj与wwq是同一个对象，因为他们在数据库中对应同一行数据(主键相同)
```

然后通过查询或flush或commit触发与数据库交互，**向数据库发出UPDATE语句**，与数据库交互

## Session.dirty

未与数据库交互前可以通过session.dirty查询到发生更改的对象：

```shell
>>> session.dirty
IdentitySet([<Account 2237169>])
```

查询或flush或commit之后：

```shell
>>> session.dirty
IdentitySet([])
```

## Session.delete()

```python
Session.delete(wwq)
```

然后通过查询或flush或commit触发与数据库交互，**向数据库发出DELETE语句**，与数据库交互

## Session.delete

未与数据库交互前可以通过session.delete查询要删除的对象：

```shell
>>> session.delete
IdentitySet([<Account 2237169>])
```

查询或flush或commit之后：

```shell
>>> session.delete
IdentitySet([])
```

# 对象状态

- **Transient** - an instance that’s not in a session, and is not saved to the database; i.e. it has no database identity. The only relationship such an object has to the ORM is that its class has a [`Mapper`](https://docs.sqlalchemy.org/en/14/orm/mapping_api.html#sqlalchemy.orm.Mapper) associated with it.尚未被session管理，在数据库中也没有对应的数据行
- **Pending** - when you [`Session.add()`](https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.add) a transient instance, it becomes pending. It still wasn’t actually flushed to the database yet, but it will be when the next flush occurs.加入session,在数据库中没有对应数据行
- **Persistent** - An instance which is present in the session and has a record in the database. You get persistent instances by either flushing so that the pending instances become persistent, or by querying the database for existing instances (or moving persistent instances from other sessions into your local session).在数据库中存在对应数据行
- **Deleted** - An instance which has been deleted within a flush, but the transaction has not yet completed. Objects in this state are essentially in the opposite of “pending” state; when the session’s transaction is committed, the object will move to the detached state. Alternatively, when the session’s transaction is rolled back, a deleted object moves *back* to the persistent state.在数据库中删除，但事务并未提交，若发生rollback可能回到persistent状态
- **Detached** - an instance which corresponds, or previously corresponded, to a record in the database, but is not currently in any session. The detached object will contain a database identity marker, however because it is not associated with a session, it is unknown whether or not this database identity actually exists in a target database. Detached objects are safe to use normally, except that they have no ability to load unloaded attributes or attributes that were previously marked as “expired”.在数据库中有对应的数据行但是对象并不属于任何一个session

# flask_sqlalchemy数据库交互

**flask_sqlalchemy是在SQLAlchemy基础上封装的库，操作可参考sqlalchemy**

以此段代码为例

```python
db = flask_sqlalchemy.SQLAlchemy()
wwq = Account(**{'account_name': 'wwq', 'addr': 'unknown', 'cell_phone': 'unknown', 'head_url': 'default.jpg', 'sex': 0, 'birthday': '2021-6-29', 'money': '99999999.99', 'create_time': '2021-06-29 20:31:28', 'update_time': '2021-06-29 20:31:28'})
db.session.add(wwq)
db.session.commit()
```

## session.add的作用

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

