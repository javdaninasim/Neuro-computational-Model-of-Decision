import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# --- بارگذاری داده‌ها ---
X = np.load("pred_amin_all.npy")   # (n_samples, 30, 30)
y_raw = np.load("y_amin_all.npy")  # مسیر فایل‌ها (برای استخراج لیبل)

# --- تخت کردن ویژگی‌ها برای SVM ---
X = X.reshape(X.shape[0], -1)  # (n_samples, 900)

# --- تبدیل y_raw (نام فایل‌ها) به لیبل عددی ---
def extract_label(filename):
    fname = filename.split("\\")[-1].lower()
    prefix = fname[:3]
    animal_prefixes = ['fda', 'fdn', 'hda', 'hdn', 'mda', 'mdn']
    return 1 if prefix in animal_prefixes else 0

y = np.array([extract_label(name) for name in y_raw])

# --- تقسیم داده به آموزش و تست ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- اجرای SVM با کرنل‌های مختلف ---
kernels = ['linear', 'rbf', 'poly']

for k in kernels:
    print(f"\n========== Kernel: {k.upper()} ==========")
    clf = SVC(kernel=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    # چاپ گزارش طبقه‌بندی کامل
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Non-Animal", "Animal"]))

    # استخراج معیارها و چاپ دستی برای گزارش
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)

    print(f"Precision : {precision:.3f}")
    print(f"Recall    : {recall:.3f}")
    print(f"F1-score  : {f1:.3f}")
    print(f"Accuracy  : {acc:.3f}")

    # نمایش ماتریس درهم‌ریختگی
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(4, 3))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                xticklabels=["Non-Animal", "Animal"], 
                yticklabels=["Non-Animal", "Animal"])
    plt.title(f"Confusion Matrix - Kernel: {k}")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    plt.show()
