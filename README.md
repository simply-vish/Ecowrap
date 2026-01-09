# 🌿 Ecowrap – Eco-Friendly Product Recommendation System

Ecowrap is a machine-learning based recommendation system that helps users make **sustainable purchasing decisions** by suggesting **more eco-friendly and biodegradable alternatives** for everyday products.

The system works using product **name or barcode**, analyzes its **biodegradability score**, and recommends better alternatives within the same category.

---

## 🚀 Features

- 🔍 Search products using **product name or barcode**
- ♻️ Displays **biodegradability score & label**
- 🧠 Recommends **eco-friendly alternatives** with higher sustainability scores
- 🧩 Intelligent category correction (e.g., snacks, beverages, dairy)
- ⚡ Fast API backend with interactive UI
- 🌱 Clean eco-themed user interface

---

## 🧠 How It Works (High Level)

1. User enters a product name or barcode  
2. System identifies the product from the dataset  
3. Determines its category and biodegradability score  
4. Filters products in the **same category**  
5. Recommends products with **higher biodegradability scores**  
6. Uses **ML-based text similarity (TF-IDF + Cosine Similarity)** as a fallback  

---

## 🛠️ Tech Stack

**Programming Language**
- Python

**Libraries & Frameworks**
- Pandas, NumPy – Data processing
- Scikit-learn – TF-IDF & Cosine Similarity
- FastAPI – Backend API
- Streamlit – Frontend UI

**Concepts Used**
- Natural Language Processing (NLP)
- Content-based Recommendation System
- Rule-based Category Classification
- REST API architecture

---

## 📊 Dataset

- Product name
- Product barcode (OpenFoodFacts `code`)
- Packaging & ingredient tags
- Ecoscore & biodegradability score
- Cleaned and corrected product categories

Dataset was extensively cleaned to fix:
- Incorrect categories
- Missing values
- Barcode formatting issues

---

## 🖥️ Application Architecture

Streamlit UI
↓
FastAPI Backend
↓
Recommendation Engine
↓
Cleaned Dataset


---

## 🎯 Use Case

Ecowrap helps consumers:
- Understand environmental impact of products
- Choose sustainable alternatives
- Reduce plastic and non-biodegradable waste

---

## 🔮 Future Enhancements

- Real barcode scanner integration
- Product image support
- Mobile application
- Deep learning-based category classification
- Carbon footprint estimation

---

## 👩‍💻 Author

**Vishakha**  
Final Year Project – Machine Learning & Sustainability

---

🌍 *Technology for a greener tomorrow.*
