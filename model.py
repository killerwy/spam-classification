import os
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

class EmailClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.models = {
            "Naive Bayes": MultinomialNB(),
            "SVM": SVC(probability=True),
            "Random Forest": RandomForestClassifier(n_estimators=100)
        }
        self.model = None
        self.trained = False
        self.data_loaded = False
        self.current_data_dir = ""
        self.emails = []
        self.labels = []

    def load_data(self, data_dir):
        """加载数据集并预处理"""
        self.current_data_dir = data_dir
        self.emails = []
        self.labels = []
        
        for folder in os.listdir(data_dir):
            folder_path = os.path.join(data_dir, folder)
            if os.path.isdir(folder_path):
                for label_type in ['ham', 'spam']:
                    label_path = os.path.join(folder_path, label_type)
                    if os.path.exists(label_path):
                        label = 0 if label_type == 'ham' else 1
                        for filename in os.listdir(label_path):
                            file_path = os.path.join(label_path, filename)
                            try:
                                with open(file_path, 'r', encoding='latin-1') as f:
                                    content = f.read()
                                    self.emails.append(self.preprocess_email(content))
                                    self.labels.append(label)
                            except:
                                continue
        
        self.data_loaded = True
        return self.emails, self.labels

    def preprocess_email(self, text):
        """预处理电子邮件文本"""
        text = text.lower()
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'<.*?>', '', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def train(self, test_size=0.2, random_state=42):
        """训练模型"""
        if not self.data_loaded:
            raise ValueError("请先加载数据")
        
        if len(self.emails) == 0:
            raise ValueError("未加载到任何邮件数据，请检查数据集路径")
        
        X_train, X_test, y_train, y_test = train_test_split(
            self.emails, self.labels, test_size=test_size, random_state=random_state
        )
        
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        results = {}
        for name, model in self.models.items():
            model.fit(X_train_vec, y_train)
            y_pred = model.predict(X_test_vec)
            
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)
            rec = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            
            results[name] = {
                'accuracy': acc,
                'precision': prec,
                'recall': rec,
                'f1': f1,
                'report': classification_report(y_test, y_pred, target_names=['正常邮件', '垃圾邮件'])
            }
        
        self.trained = True
        return results

    def predict(self, email_text, model_name="Naive Bayes"):
        """预测邮件类别"""
        if not self.trained:
            raise RuntimeError("请先训练模型")
        
        self.model = self.models.get(model_name)
        if self.model is None:
            raise ValueError(f"未知模型: {model_name}")
        
        processed_text = self.preprocess_email(email_text)
        text_vec = self.vectorizer.transform([processed_text])
        
        prediction = self.model.predict(text_vec)
        probability = self.model.predict_proba(text_vec)[0]
        
        return "垃圾邮件" if prediction[0] == 1 else "正常邮件", probability
