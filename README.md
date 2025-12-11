# Compiler Project -- Scanner & Top‑Down Parser (LL Parser)

## 📌 مقدمة

هذا المشروع عبارة عن **Compiler Front-End** بسيط مكوّن من مرحلتين
رئيسيتين:

1.  **الـScanner (Lexical Analyzer)**\
    مسؤول عن قراءة الكود المصدري واستخراج الـTokens (مثل الكلمات
    المحجوزة، المعرفات، الأرقام، المعاملات، والتعليقات...).

2.  **الـParser (Syntax Analyzer)**\
    يأخذ الـTokens الناتجة من الـScanner ويحدد إذا كان الكود صحيح نحويًا
    (Syntax Correct) أو يحتوي على Syntax Error.

يتم تطبيق الـParser هنا باستخدام **Top‑Down Recursive Descent Parsing**.

------------------------------------------------------------------------

## 📂 مكوّنات المشروع

### 1️⃣ ملف scanner.py

هذا الملف مسؤول عن: - قراءة الكود من ملف C. - التعرّف على: - الكلمات
المحجوزة (Keywords) - المعرفات (Identifiers) - الأرقام (Numeric
Constants) - المعاملات (Operators) - الرموز الخاصة (Special
Characters) - التعليقات (Single-line & Multi-line) - تخزين الـTokens في
ملف مثل:\
`test_tokens.txt`

### **أهم مميزات الـScanner**

-   يدعم التعليقات بنوعيها:
    -   `// single line`
    -   `/* multi line */`
-   يدعم الأعداد الصحيحة والعشرية.
-   يفرّق بين **keywords** و **identifiers**.
-   يطبع كل Token بنوعه وقيمته.

------------------------------------------------------------------------

### 2️⃣ ملف parser_Top_down.py

هذا الملف ينفذ **Top‑Down Parser** يقوم بـ: - قراءة الـTokens من ملف
`test_tokens.txt`. - تجاهل التعليقات. - تنفيذ قواعد اللغة (Grammar)
التالية بشكل تقريبي:

#### **Grammar Supported**

    Program        → int main ( ) { CodeBlock }
    CodeBlock      → { Statement* }
    Statement      → Declaration | Assignment | IfStatement | ReturnStatement
    Declaration    → int id (, id)* ;
    Assignment     → id = Expression ;
    IfStatement    → if ( Expression ) CodeBlock (else CodeBlock)?
    ReturnStatement→ return (id | num) ;
    Expression     → Term (relop Term)?
    Term           → Factor ((+ | -) Factor)*
    Factor         → id | num

------------------------------------------------------------------------

## 🧪 مثال التشغيل

### **الكود المدخل**

``` c
int main() {
    int x ,y;
    // This is a single-line comment
    if (x == 42) {
        /* block comment */
        x = x-3;
    } else {
        y = 3.1; // Another comment
    }
    return 0;
}
```

### **ناتج الـScanner (باختصار)**

    1    KEYWORD              int
    2    KEYWORD              main
    3    SPECIAL_CHARACTER    (
    4    SPECIAL_CHARACTER    )
    5    SPECIAL_CHARACTER    {
    ...
    37   SPECIAL_CHARACTER    }
    Total tokens: 37

### **ناتج الـParser**

    Parsing Completed Successfully. No Syntax Errors Found.

------------------------------------------------------------------------

## ⚠️ في حالة وجود خطأ نحوي

سيطبع الـParser رسالة مثل:

    Syntax Error! Expected: (;) but found: (Type: IDENTIFIER, Value: x) at token index 14

------------------------------------------------------------------------

## ▶️ طريقة الاستخدام

### **1. تشغيل الـScanner**

    python scanner.py input.c

الملف الناتج سيكون:

    input_tokens.txt

### **2. تشغيل الـParser**

تأكد أن ملف التوكن اسمه:

    test_tokens.txt

ثم شغّل:

    python parser_Top_down.py

------------------------------------------------------------------------

## 📌 ملاحظات مهمة

-   أي تعليق يتم تجاهله بواسطة الـParser.
-   الـParser يعتمد على الترتيب الصحيح للـTokens.
-   لو عايز تدعم أنواع إضافية (float, double, char...) يمكن إضافتها
    بسهولة في الـScanner & Parser.

------------------------------------------------------------------------

## ✔️ الخلاصة

هذا المشروع يحاكي أول مرحلتين من بناء Compilers: - **Lexical
Analysis** - **Syntax Analysis**

ويدعم بنية C-style programs مع أمثلة وتصميم واضح وقابل للتطوير.


