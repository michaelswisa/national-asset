# אפיון מבנה טבלאות - מערכת ניהול לוחמים

## 1. טבלת Users
מכילה את כל המשתמשים במערכת (חיילים, מפקדים, מנהלים).

| שדה | סוג | מאפיינים | תיאור |
|------|------|------------|--------|
| user_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | מזהה ייחודי למשתמש |
| username | VARCHAR(50) | UNIQUE, NOT NULL | שם משתמש |
| password_hash | VARCHAR(255) | NOT NULL | הצפנת הסיסמה |
| email | VARCHAR(100) | UNIQUE, NOT NULL | כתובת אימייל |
| role | ENUM('soldier', 'commander', 'manager') | NOT NULL | תפקיד המשתמש במערכת |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | זמן יצירת המשתמש |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | זמן עדכון אחרון |

## 2. טבלת Soldiers
מכילה מידע ספציפי לחיילים.

| שדה | סוג | מאפיינים | תיאור |
|------|------|------------|--------|
| soldier_id | INTEGER | PRIMARY KEY | מזהה ייחודי לחייל (מקושר ל-user_id) |
| personal_number | VARCHAR(20) | UNIQUE, NOT NULL | מספר אישי של החייל |
| first_name | VARCHAR(50) | NOT NULL | שם פרטי |
| last_name | VARCHAR(50) | NOT NULL | שם משפחה |
| phone_number | VARCHAR(20) | | מספר טלפון |
| is_kosher | BOOLEAN | DEFAULT FALSE | האם כשר |
| receive_sms | BOOLEAN | DEFAULT TRUE | האם מקבל הודעות SMS |
| whatsapp_enabled | BOOLEAN | DEFAULT FALSE | האם מחובר ל-WhatsApp |
| unit_id | INTEGER | FOREIGN KEY | מזהה היחידה אליה משויך החייל |

## 3. טבלת Commanders
מכילה מידע ספציפי למפקדים.

| שדה | סוג | מאפיינים | תיאור |
|------|------|------------|--------|
| commander_id | INTEGER | PRIMARY KEY | מזהה ייחודי למפקד (מקושר ל-user_id) |
| rank | VARCHAR(50) | NOT NULL | דרגת המפקד |
| unit_id | INTEGER | FOREIGN KEY | מזהה היחידה עליה אחראי המפקד |

## 4. טבלת Units
מכילה מידע על היחידות והמחלקות.

| שדה | סוג | מאפיינים | תיאור |
|------|------|------------|--------|
| unit_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | מזהה ייחודי ליחידה |
| unit_name | VARCHAR(100) | NOT NULL | שם היחידה |
| parent_unit_id | INTEGER | FOREIGN KEY (SELF REFERENCE) | מזהה היחידה הבכירה (אם יש) |

## 5. טבלת Addresses
מכילה כתובות של חיילים (מאפשר ריבוי כתובות לחייל).

| שדה | סוג | מאפיינים | תיאור |
|------|------|------------|--------|
| address_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | מזהה ייחודי לכתובת |
| soldier_id | INTEGER | FOREIGN KEY | מזהה החייל |
| address_type | ENUM('home', 'mailing', 'emergency') | NOT NULL | סוג הכתובת |
| street | VARCHAR(100) | NOT NULL | שם הרחוב |
| city | VARCHAR(50) | NOT NULL | שם העיר |
| state | VARCHAR(50) | | שם המדינה/מחוז |
| postal_code | VARCHAR(20) | | מיקוד |

## 6. טבלת Tasks
מכילה משימות שנוצרו על ידי מפקדים.

| שדה | סוג | מאפיינים | תיאור |
|------|------|------------|--------|
| task_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | מזהה ייחודי למשימה |
| creator_id | INTEGER | FOREIGN KEY (Users) | מזהה המפקד שיצר את המשימה |
| title | VARCHAR(100) | NOT NULL | כותרת המשימה |
| description | TEXT | | תיאור מפורט של המשימה |
| status | ENUM('pending', 'in_progress', 'completed', 'cancelled') | NOT NULL | סטטוס המשימה |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | זמן יצירת המשימה |
| due_date | DATE | | תאריך יעד לסיום המשימה |

## 7. טבלת Task_Assignments
מקשרת בין משימות לחיילים (מאפשר הקצאת משימה למספר חיילים).

| שדה | סוג | מאפיינים | תיאור |
|------|------|------------|--------|
| assignment_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | מזהה ייחודי להקצאה |
| task_id | INTEGER | FOREIGN KEY (Tasks) | מזהה המשימה |
| soldier_id | INTEGER | FOREIGN KEY (Soldiers) | מזהה החייל |
| assigned_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | זמן הקצאת המשימה |

## 8. טבלת Locations
מכילה מידע על מיקומי החיילים.

| שדה | סוג | מאפיינים | תיאור              |
|------|------|------------|--------------------|
| location_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | מזהה ייחודי למיקום |
| soldier_id | INTEGER | FOREIGN KEY (Soldiers) | מזהה החייל         |
| latitude | DECIMAL(10, 8) | | קו רוחב            |
| longitude | DECIMAL(11, 8) | | קו אורך            |
| full_address | VARCHAR(255) | NOT NULL | כתובת מלאה         |
| timestamp | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | זמן עדכון המיקום   |

## הערות לגבי הנרמול:
1. הטבלאות מנורמלות לפי עקרונות ה-3NF (Third Normal Form):
   - כל טבלה מכילה מידע על נושא אחד בלבד.
   - כל שדה שאינו מפתח תלוי באופן מלא במפתח הראשי.
   - אין תלויות בין שדות שאינם מפתח.

2. השתמשנו בטבלאות קשר (כמו Task_Assignments) כדי לייצג יחסים של many-to-many.

3. מידע חוזר (כמו כתובות) הועבר לטבלה נפרדת (Addresses) עם קשר לטבלת Soldiers.

4. השתמשנו ב-ENUM לשדות עם ערכים קבועים מראש, כמו סטטוס משימה או סוג כתובת.

5. הוספנו שדות timestamp לתיעוד זמני יצירה ועדכון ברשומות רלוונטיות.

מבנה זה מאפשר גמישות, יעילות בשאילתות, ומניעת כפילות מידע, תוך שמירה על היכולת לייצג את כל המידע הנדרש במערכת.
