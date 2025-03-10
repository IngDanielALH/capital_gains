# 📊 Capital Gains Calculator  

This project implements a system to calculate capital gains based on buy and sell transactions of assets. It determines applicable taxes according to established regulations.  

## 🚀 Features  

- Calculation of **weighted average price** for purchases.  
- Determination of **gains and losses** on sales.  
- Application of **taxes** based on configurable thresholds and rates.  
- **Unit tests** to validate calculations.  

## 🛠️ Installation  
The project was tested using Python 3.9.6 🐍

**Required dependencies**:  
   ```bash
   pip install pyyaml
   ```  
```bash
pip install pytest
   ```  

## 📝 Usage  

Capital gains are calculated based on a list of transactions that include details about the operation, unit cost, and quantity.  

### **Input Example**  
```json
[
    {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
    {"operation": "sell", "unit-cost": 2.00, "quantity": 5000},
    {"operation": "sell", "unit-cost": 20.00, "quantity": 2000},
    {"operation": "sell", "unit-cost": 20.00, "quantity": 2000},
    {"operation": "sell", "unit-cost": 25.00, "quantity": 1000}
]
```  

### **Expected Output**  
```json
[
    {"tax": 0.00},
    {"tax": 0.00},
    {"tax": 0.00},
    {"tax": 0.00},
    {"tax": 3000.00}
]
```  

## 🧪 Testing  

To run unit tests, use:  
```bash
python -m pytest tests/ 
```  

### **Expected Output**  
```
====================================== test session starts ============================================================
platform darwin -- Python 3.9.6, pytest-8.3.5, pluggy-1.5.0
rootdir: /Users/danielalejandrolopezhernandez/Documents/Proyectos/Python/capital_gains
collected 12 items                                                                                                                                                                                                                                      

tests/integration_tests/test_gain_service.py .........                                                                                                                                                                                           [ 75%]
tests/integration_tests/test_main_function.py ..                                                                                                                                                                                                 [ 91%]
tests/unit_tests/test_round.py .                                                                                                                                                                                                                 [100%]

====================================== 12 passed in 0.14s ==============================================================
```  

## 📌 Configuration  

The calculation behavior can be modified by adjusting the following parameters in the YAML file:  

- **`tax_percentage`**: Applicable tax percentage.  
- **`limit_without_tax`**: Threshold beyond which tax is applied.  

### 📂 Using `pyyaml` for Dynamic Configuration  

The project uses `pyyaml` to manage configuration values, such as tax rates and tax-free limits, which may change over 
time. This allows:  

- Keeping configurable values separate from the code.  
- Facilitating updates without modifying the source code.  
- Improving system reusability and adaptability to regulatory changes.  
  (The YAML file is located in the root of this project.)

Example YAML file:  
```yaml
tax_percentage: 20
limit_without_tax: 20000
```  

## ▶️ Running the Project  

To run the project from the terminal, it is recommended to redirect the input as follows:  

```bash
./main.py < input.txt
```
A sample input file is available at `tests/resources/input.txt`.