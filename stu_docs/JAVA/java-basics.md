# Java基础知识教程

## 1. Java语言特性

### 1.1 面向对象
- Java是一种纯面向对象的编程语言
- 所有代码都必须在类中编写
- 支持封装、继承、多态三大特性

### 1.2 平台无关性
- Java代码编译为字节码(.class文件)
- JVM(Java虚拟机)负责执行字节码
- "一次编写，到处运行"的特性

### 1.3 健壮性
- 强类型检查
- 自动内存管理(垃圾回收)
- 异常处理机制

### 1.4 安全性
- 字节码验证
- 沙箱安全模型
- 类加载器机制

### 1.5 多线程
- 内置多线程支持
- 同步机制
- 线程池

## 2. 基础语法

### 2.1 数据类型

#### 基本数据类型
- 整型：byte, short, int, long
- 浮点型：float, double
- 字符型：char
- 布尔型：boolean

#### 引用数据类型
- 类(Class)
- 接口(Interface)
- 数组(Array)

### 2.2 变量与常量

```java
// 变量声明与初始化
int age = 20;
String name = "Java";

// 常量声明
final double PI = 3.14159;
```

### 2.3 运算符
- 算术运算符：+, -, *, /, %, ++, --
- 关系运算符：==, !=, >, <, >=, <=
- 逻辑运算符：&&, ||, !
- 位运算符：&, |, ^, ~, <<, >>, >>>
- 赋值运算符：=, +=, -=, *=, /=, %=
- 条件运算符：?:

### 2.4 控制流

#### 条件语句
```java
if (condition) {
    // 代码块
} else if (anotherCondition) {
    // 代码块
} else {
    // 代码块
}

switch (variable) {
    case value1:
        // 代码块
        break;
    case value2:
        // 代码块
        break;
    default:
        // 代码块
}
```

#### 循环语句
```java
// for循环
for (int i = 0; i < 10; i++) {
    // 代码块
}

// while循环
while (condition) {
    // 代码块
}

// do-while循环
do {
    // 代码块
} while (condition);
```

### 2.5 数组

```java
// 一维数组
int[] numbers = new int[5];
int[] numbers2 = {1, 2, 3, 4, 5};

// 二维数组
int[][] matrix = new int[3][3];
int[][] matrix2 = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
```

## 3. 面向对象编程概念

### 3.1 类与对象

```java
// 类的定义
public class Person {
    // 成员变量
    private String name;
    private int age;
    
    // 构造方法
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // 成员方法
    public void sayHello() {
        System.out.println("Hello, my name is " + name);
    }
    
    // getter和setter方法
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
}

// 对象的创建与使用
Person person = new Person("Alice", 25);
person.sayHello();
```

### 3.2 封装
- 将数据和方法包装在类中
- 通过访问修饰符控制访问权限
- 提供getter和setter方法访问和修改数据

### 3.3 继承
```java
// 父类
public class Animal {
    public void eat() {
        System.out.println("Animal eats");
    }
}

// 子类
public class Dog extends Animal {
    @Override
    public void eat() {
        System.out.println("Dog eats bones");
    }
    
    public void bark() {
        System.out.println("Dog barks");
    }
}
```

### 3.4 多态
- 方法重写(Override)
- 方法重载(Overload)
- 向上转型

### 3.5 抽象类与接口

```java
// 抽象类
public abstract class Shape {
    public abstract double calculateArea();
}

// 接口
public interface Drawable {
    void draw();
}

// 实现类
public class Circle extends Shape implements Drawable {
    private double radius;
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
    
    @Override
    public void draw() {
        System.out.println("Drawing a circle");
    }
}
```

## 4. 常用类库

### 4.1 java.lang包
- Object：所有类的父类
- String：字符串处理
- Integer, Double等包装类
- Math：数学运算
- System：系统相关
- Thread：线程相关

### 4.2 java.util包
- Collection框架：List, Set, Map
- Date, Calendar：日期时间
- Scanner：输入处理
- Random：随机数生成

### 4.3 java.io包
- File：文件操作
- InputStream, OutputStream：字节流
- Reader, Writer：字符流

### 4.4 java.net包
- URL：统一资源定位符
- Socket：网络通信

### 4.5 java.sql包
- Connection：数据库连接
- Statement：SQL语句执行
- ResultSet：结果集处理

## 5. 异常处理

```java
try {
    // 可能抛出异常的代码
    int result = 10 / 0;
} catch (ArithmeticException e) {
    // 捕获异常并处理
    System.out.println("除数不能为零");
} finally {
    // 无论是否发生异常都会执行的代码
    System.out.println("执行finally块");
}
```

## 6. 泛型

```java
// 泛型类
public class Box<T> {
    private T content;
    
    public void setContent(T content) {
        this.content = content;
    }
    
    public T getContent() {
        return content;
    }
}

// 使用泛型
Box<String> stringBox = new Box<>();
stringBox.setContent("Hello");
String content = stringBox.getContent();
```

## 7. 集合框架

```java
// List
List<String> list = new ArrayList<>();
list.add("Java");
list.add("Python");
list.add("C++");

// Set
Set<String> set = new HashSet<>();
set.add("Java");
set.add("Python");
set.add("Java"); // 重复元素不会被添加

// Map
Map<String, Integer> map = new HashMap<>();
map.put("Java", 1);
map.put("Python", 2);
map.put("C++", 3);
```

## 8. 输入输出

```java
// 输入
Scanner scanner = new Scanner(System.in);
System.out.print("请输入你的名字：");
String name = scanner.nextLine();
System.out.println("你好，" + name);

// 输出
System.out.println("Hello World");
System.out.printf("%s的年龄是%d岁\n", name, 20);
```

## 9. 多线程

```java
// 继承Thread类
class MyThread extends Thread {
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println("Thread: " + i);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}

// 实现Runnable接口
class MyRunnable implements Runnable {
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println("Runnable: " + i);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}

// 使用
MyThread thread = new MyThread();
thread.start();

Thread runnableThread = new Thread(new MyRunnable());
runnableThread.start();
```

## 10. 反射

```java
// 获取类的Class对象
Class<?> clazz = Person.class;

// 获取类的名称
String className = clazz.getName();

// 获取类的方法
Method[] methods = clazz.getDeclaredMethods();

// 获取类的字段
Field[] fields = clazz.getDeclaredFields();

// 创建对象
Person person = (Person) clazz.newInstance();

// 调用方法
Method method = clazz.getDeclaredMethod("sayHello");
method.invoke(person);
```

## 11. 注解

```java
// 定义注解
@interface MyAnnotation {
    String value() default "";
    int number() default 0;
}

// 使用注解
@MyAnnotation(value = "Test", number = 1)
public class TestClass {
    @MyAnnotation(value = "Field")
    private String field;
    
    @MyAnnotation(value = "Method")
    public void method() {
    }
}
```

## 12. Lambda表达式

```java
// 传统方式
Runnable runnable1 = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello");
    }
};

// Lambda表达式
Runnable runnable2 = () -> System.out.println("Hello");

// 带参数的Lambda表达式
BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;
int result = add.apply(1, 2);

// 带多行代码的Lambda表达式
Consumer<String> consumer = (s) -> {
    System.out.println("Hello");
    System.out.println(s);
};
consumer.accept("World");
```

## 13. Stream API

```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");

// 过滤
List<String> filteredNames = names.stream()
    .filter(name -> name.length() > 3)
    .collect(Collectors.toList());

// 映射
List<Integer> nameLengths = names.stream()
    .map(String::length)
    .collect(Collectors.toList());

// 排序
List<String> sortedNames = names.stream()
    .sorted()
    .collect(Collectors.toList());

// 聚合
Optional<String> longestName = names.stream()
    .max(Comparator.comparingInt(String::length));

// 统计
long count = names.stream()
    .filter(name -> name.startsWith("A"))
    .count();
```

## 14. 模块系统

```java
// module-info.java
module com.example.myapp {
    requires java.base;
    requires java.sql;
    exports com.example.myapp.model;
    exports com.example.myapp.service;
}
```

## 15. 日期时间API

```java
// LocalDate
LocalDate today = LocalDate.now();
LocalDate tomorrow = today.plusDays(1);
LocalDate specificDate = LocalDate.of(2023, 12, 25);

// LocalTime
LocalTime now = LocalTime.now();
LocalTime specificTime = LocalTime.of(12, 30, 45);

// LocalDateTime
LocalDateTime dateTime = LocalDateTime.now();
LocalDateTime specificDateTime = LocalDateTime.of(2023, 12, 25, 12, 30, 45);

// DateTimeFormatter
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String formattedDateTime = dateTime.format(formatter);
LocalDateTime parsedDateTime = LocalDateTime.parse("2023-12-25 12:30:45", formatter);
```

## 16. 最佳实践

1. 命名规范：类名使用驼峰命名法，方法名和变量名使用小驼峰命名法，常量使用全大写
2. 代码风格：适当的缩进，合理的空行，清晰的注释
3. 异常处理：合理捕获和处理异常，避免空catch块
4. 内存管理：避免内存泄漏，合理使用集合
5. 性能优化：避免不必要的对象创建，合理使用缓存
6. 安全性：避免SQL注入，使用参数化查询，注意输入验证

## 17. 开发工具

- JDK：Java开发工具包
- IDE：Eclipse, IntelliJ IDEA, NetBeans
- 构建工具：Maven, Gradle
- 版本控制：Git
- 测试工具：JUnit, TestNG
- 代码质量：SonarQube

## 18. 学习资源

- 官方文档：https://docs.oracle.com/en/java/
- 书籍：《Java核心技术》《Effective Java》
- 在线教程：Oracle Java Tutorials, MOOC课程
- 社区：Stack Overflow, GitHub

---

本教程涵盖了Java基础知识的核心内容，希望对您的学习有所帮助。如有任何问题，请随时查阅官方文档或参考相关资源。