# SQL-CRUD 基础



# Select语句

假设我们有以下 `employees` 表：

```
| id   | first_name | last_name | email                  | department | salary |
| ---- | ---------- | --------- | ---------------------- | ---------- | ------ |
| 1    | John       | Doe       | john.doe@example.com   | Sales      | 50000  |
| 2    | Jane       | Smith     | jane.smith@example.com | Marketing  | 60000  |
| 3    | Mike       | Johnson   | mike.j@example.com     | IT         | 65000  |
| 4    | Sarah      | Williams  | sarah.w@example.com    | HR         | 55000  |
| 5    | David      | Brown     | david.b@example.com    | Sales      | 52000  |
```

现在，让我们看一些 SELECT 语句及其执行结果：

1. 检索特定列：
```sql
SELECT first_name, last_name FROM employees;
```
结果：
```
first_name | last_name
-----------|-----------
John       | Doe
Jane       | Smith
Mike       | Johnson
Sarah      | Williams
David      | Brown
```

2. 检索所有列：
```sql
SELECT * FROM employees;
```
结果：
```
id | first_name | last_name | email                  | department | salary
---|------------|-----------|------------------------|------------|-------
1  | John       | Doe       | john.doe@example.com   | Sales      | 50000
2  | Jane       | Smith     | jane.smith@example.com | Marketing  | 60000
3  | Mike       | Johnson   | mike.j@example.com     | IT         | 65000
4  | Sarah      | Williams  | sarah.w@example.com    | HR         | 55000
5  | David      | Brown     | david.b@example.com    | Sales      | 52000
```

3. 检索不同的值（去重）：
```sql
SELECT DISTINCT department FROM employees;
```
结果：
```
department
----------
Sales
Marketing
IT
HR
```

4. 为列指定别名：
```sql
SELECT first_name AS "First Name", last_name AS "Last Name" FROM employees;
```
结果：
```
First Name | Last Name
-----------|----------
John       | Doe
Jane       | Smith
Mike       | Johnson
Sarah      | Williams
David      | Brown
```

5. 使用简单的计算：
```sql
SELECT first_name, salary, salary * 1.1 AS "New Salary" FROM employees;
```
结果：
```
first_name | salary | New Salary
-----------|--------|------------
John       | 50000  | 55000
Jane       | 60000  | 66000
Mike       | 65000  | 71500
Sarah      | 55000  | 60500
David      | 52000  | 57200
```



# CREATE TABLE

CREATE TABLE 的基本语法：
```sql
CREATE TABLE table_name (
    column1 datatype constraints,
    column2 datatype constraints,
    ...,
    table_constraints
);
```

让我们通过一个例子来说明 CREATE TABLE 的用法，然后我会给出执行结果。

假设我们要创建一个 `employees` 表：

```sql
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE,
    department VARCHAR(50),
    salary DECIMAL(10, 2)
);
```

这个语句做了以下几件事：
1. 创建了一个名为 `employees` 的新表。
2. 定义了多个列，每列都有其数据类型和约束。
3. 设置 `id` 为主键，并使用 AUTO_INCREMENT 使其自动增长。
4. 将 `first_name` 和 `last_name` 设为 NOT NULL，表示这些字段不能为空。
5. 将 `email` 设为 UNIQUE，确保每个邮箱地址都是唯一的。

执行结果：
当你执行这个 CREATE TABLE 语句后，数据库会创建表，但不会直接显示任何结果。然而，你可以使用 DESCRIBE 或 SHOW COLUMNS 命令来查看新创建的表结构：

```sql
DESCRIBE employees;
```

或

```sql
SHOW COLUMNS FROM employees;
```

这两个命令的结果类似，会显示如下信息：

```
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | int          | NO   | PRI | NULL    | auto_increment |
| first_name | varchar(50)  | NO   |     | NULL    |                |
| last_name  | varchar(50)  | NO   |     | NULL    |                |
| email      | varchar(100) | YES  | UNI | NULL    |                |
| hire_date  | date         | YES  |     | NULL    |                |
| department | varchar(50)  | YES  |     | NULL    |                |
| salary     | decimal(10,2)| YES  |     | NULL    |                |
+------------+--------------+------+-----+---------+----------------+
```

这个结果显示了表的结构，包括每个列的名称、数据类型、是否可以为空、键类型、默认值和其他额外信息。

CREATE TABLE 语句的其他重要特性：

1. 外键约束：
   ```sql
   CREATE TABLE orders (
       order_id INT PRIMARY KEY,
       customer_id INT,
       order_date DATE,
       FOREIGN KEY (customer_id) REFERENCES customers(id)
   );
   ```

2. 检查约束：
   ```sql
   CREATE TABLE products (
       id INT PRIMARY KEY,
       name VARCHAR(100),
       price DECIMAL(10, 2) CHECK (price > 0)
   );
   ```

3. 默认值：
   ```sql
   CREATE TABLE users (
       id INT PRIMARY KEY,
       username VARCHAR(50),
       is_active BOOLEAN DEFAULT TRUE
   );
   ```

CREATE 语句是 SQL 中非常重要的一部分，它允许你定义数据库的结构。正确使用 CREATE TABLE 可以确保你的数据以一种有组织、高效和一致的方式存储。在实际应用中，创建表时要仔细考虑数据类型、约束和索引，以优化数据库性能和维护数据完整性。

# INSERT 

我们使用上面CREATE TABLE 创建的表格

```sql
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE,
    department VARCHAR(50),
    salary DECIMAL(10, 2)
);
```

现在，让我们看几种使用 INSERT 语句的方式：

1. 插入完整的行数据：

```sql
INSERT INTO employees (first_name, last_name, email, hire_date, department, salary)
VALUES ('John', 'Doe', 'john.doe@example.com', '2023-01-15', 'Sales', 50000.00);
```

注意，我们没有指定 `id`，因为它是自动增长的。

2. 插入部分列数据（未指定的列将使用默认值或 NULL）：

```sql
INSERT INTO employees (first_name, last_name, email, department)
VALUES ('Jane', 'Smith', 'jane.smith@example.com', 'Marketing');
```

3. 一次插入多行数据：

```sql
INSERT INTO employees (first_name, last_name, email, hire_date, department, salary)
VALUES 
    ('Mike', 'Johnson', 'mike.j@example.com', '2023-02-01', 'IT', 65000.00),
    ('Sarah', 'Williams', 'sarah.w@example.com', '2023-02-15', 'HR', 55000.00),
    ('David', 'Brown', 'david.b@example.com', '2023-03-01', 'Sales', 52000.00);
```

执行这些 INSERT 语句后，我们可以使用 SELECT 语句来查看插入的数据：

```sql
SELECT * FROM employees;
```

执行结果将如下所示：

```
+----+------------+-----------+---------------------------+------------+------------+----------+
| id | first_name | last_name | email                     | hire_date  | department | salary   |
+----+------------+-----------+---------------------------+------------+------------+----------+
|  1 | John       | Doe       | john.doe@example.com      | 2023-01-15 | Sales      | 50000.00 |
|  2 | Jane       | Smith     | jane.smith@example.com    | NULL       | Marketing  | NULL     |
|  3 | Mike       | Johnson   | mike.j@example.com        | 2023-02-01 | IT         | 65000.00 |
|  4 | Sarah      | Williams  | sarah.w@example.com       | 2023-02-15 | HR         | 55000.00 |
|  5 | David      | Brown     | david.b@example.com       | 2023-03-01 | Sales      | 52000.00 |
+----+------------+-----------+---------------------------+------------+------------+----------+
```

注意事项：

1. 自动增长的 `id` 列：数据库自动为每一行分配了唯一的 id。

2. NULL 值：对于 Jane Smith，我们没有提供 `hire_date` 和 `salary`，所以这些字段显示为 NULL。

3. 非空约束：我们必须为 `first_name` 和 `last_name` 提供值，因为它们被定义为 NOT NULL。

4. 唯一约束：每个 `email` 必须是唯一的。如果你尝试插入一个已存在的 email，会得到一个错误。

5. 数据类型匹配：插入的值必须与定义的数据类型相匹配。例如，`salary` 必须是一个数值。

INSERT 语句的其他用法：

1. 从其他表插入数据：

```sql
INSERT INTO new_employees (first_name, last_name, email)
SELECT first_name, last_name, email
FROM employees
WHERE department = 'Sales';
```

2. 使用 SET 语法（适用于单行插入）：

```sql
INSERT INTO employees
SET first_name = 'Alice', 
    last_name = 'Johnson', 
    email = 'alice.j@example.com', 
    department = 'Finance';
```

INSERT 语句是数据操作语言（DML）的一个重要组成部分，它允许我们向数据库中添加新的数据。正确使用 INSERT 语句可以确保数据的完整性和一致性。在实际应用中，INSERT 语句通常与应用程序代码集成，用于处理用户输入或从其他数据源导入数据。