import tkinter as tk
from tkinter import ttk, messagebox

class EquationSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Equation Solver")
        self.root.geometry("600x400")
        
        # Variables
        self.current_inputs = []
        self.input_values = {}
        
        # Main Frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Target Selection
        ttk.Label(main_frame, text="Solve for:").grid(row=0, column=0, sticky=tk.W)
        self.target_var = tk.StringVar()
        targets = ['T', 'W', 'F', 'm', 'S*', 'S', 'C1', 'C2', 'd', 'v']  # Added 'd' and 'v'
        target_combo = ttk.Combobox(main_frame, textvariable=self.target_var, values=targets)
        target_combo.grid(row=0, column=1, sticky=tk.W)
        target_combo.bind('<<ComboboxSelected>>', self.update_inputs)
        
        # Method selection for W (initially hidden)
        self.method_frame = ttk.Frame(main_frame)
        self.method_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        self.method_var = tk.StringVar(value="1")
        ttk.Radiobutton(self.method_frame, text="สัมประสิทธิ์ไม้กายสิทธิ์ (จากสูตรแปลงกลาย)", variable=self.method_var, 
                       value="1", command=self.update_inputs).grid(row=0, column=0)
        ttk.Radiobutton(self.method_frame, text="สัมประสิทธิ์ไม้กายสิทธิ์ (จากสูตรไม้กายสิทธิ์)", variable=self.method_var, 
                       value="2", command=self.update_inputs).grid(row=0, column=1)
        self.method_frame.grid_remove()
        
        # Input Frame
        self.input_frame = ttk.Frame(main_frame)
        self.input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Calculate Button
        ttk.Button(main_frame, text="Calculate", command=self.calculate).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Result Label
        self.result_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.result_var, font=('Arial', 12, 'bold')).grid(row=4, column=0, columnspan=2)
        
    def update_inputs(self, event=None):
        # Clear previous inputs
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.current_inputs = []
        self.input_values = {}
        
        target = self.target_var.get()
        if not target:
            return
            
        # Show/hide method selection for W
        if target == 'W':
            self.method_frame.grid()
        else:
            self.method_frame.grid_remove()
        
        # Define required inputs based on target
        if target == 'd':  # New case for density
            self.add_input_field('m (มวล)')
            self.add_input_field('v (ปริมาตร)')
        elif target == 'v':  # New case for volume
            self.add_input_field('m (มวล)')
            self.add_input_field('d (ความหนาแน่น)')
        elif target == 'm' :  # Direct m calculation
            self.add_input_field('d (ความหนาแน่น)')
            self.add_input_field('v (ปริมาตร)')
        elif target == 'T':
            self.add_input_field('W (สัมประสิทธิ์ของไม้กายสิทธิ์)')
            self.add_input_field('F (แรงในการร่าย)')
            self.add_m_input()
            self.add_input_field('S* (ค่าสถานะทางสสารใหม่)')
        elif target == 'W':
            if self.method_var.get() == "1":
                self.add_input_field('T (ค่าในการเปลี่ยนรูป)')
                self.add_input_field('F (แรงในการร่าย)')
                self.add_m_input()
                self.add_input_field('S* (ค่าสถานะทางสสารใหม่)')
            else:
                self.add_input_field('a (ค่าสัมประสิทธิ์วัสดุ)')
                self.add_input_field('b (ค่าสัมประสิทธิ์แกนกลางไม้กายสิทธิ์)')
                self.add_input_field('L (ความยาวของไม้กายสิทธิ์)')
                self.add_input_field('f (ค่าความยืดหยุ่นของไม้กายสิทธิ์)')
        elif target in ['F', 'S*']:
            self.add_input_field('T (ค่าในการเปลี่ยนรูป)')
            self.add_input_field('W (สัมประสิทธิ์ของไม้กายสิทธิ์)')
            self.add_m_input()
            if target == 'F':
                self.add_input_field('S* (ค่าสถานะทางสสารใหม่)')
            else:
                self.add_input_field('F (แรงในการร่าย)')
        elif target == 'S':
            self.add_input_field('S* (ค่าสถานะทางสสารใหม่)')
            self.add_input_field('C1 (อุณหภูมิก่อนแปลงสภาพ)')
            self.add_input_field('C2 (อุณหภูมิหลังแปลงสภาพ)')
        elif target in ['C1', 'C2']:
            self.add_input_field('o (ค่าของ |ΔC| /10)')
            self.add_input_field('C2 (อุณหภูมิหลังแปลงสภาพ)' if target == 'C1' else 'C1 (อุณหภูมิก่อนแปลงสภาพ)')
    
    def add_input_field(self, label):
        row = len(self.current_inputs)
        ttk.Label(self.input_frame, text=f"{label}:").grid(row=row, column=0, padx=5, pady=2)
        var = tk.StringVar()
        entry = ttk.Entry(self.input_frame, textvariable=var)
        entry.grid(row=row, column=1, padx=5, pady=2)
        self.current_inputs.append((label.split()[0], var))
        
    def add_m_input(self):
        row = len(self.current_inputs)
        frame = ttk.Frame(self.input_frame)
        frame.grid(row=row, column=0, columnspan=2, pady=5)
        
        # m direct input
        var_m = tk.StringVar()
        self.current_inputs.append(('m', var_m))
        ttk.Label(frame, text="m (มวล):").grid(row=0, column=0, padx=5)
        entry_m = ttk.Entry(frame, textvariable=var_m)
        entry_m.grid(row=0, column=1, padx=5)
        
        # or label
        ttk.Label(frame, text="or").grid(row=1, column=0, columnspan=2, pady=2)
        
        # d and v inputs
        var_d = tk.StringVar()
        var_v = tk.StringVar()
        self.current_inputs.append(('d', var_d))
        self.current_inputs.append(('v', var_v))
        
        ttk.Label(frame, text="d (ความหนาแน่น):").grid(row=2, column=0, padx=5)
        ttk.Entry(frame, textvariable=var_d).grid(row=2, column=1, padx=5)
        
        ttk.Label(frame, text="v (ปริมาตร):").grid(row=3, column=0, padx=5)
        ttk.Entry(frame, textvariable=var_v).grid(row=3, column=1, padx=5)
    
    def calculate(self):
        try:
            target = self.target_var.get()
            if not target:
                messagebox.showerror("Error", "Please select what to solve for")
                return
                
            # Get input values
            values = {}
            for label, var in self.current_inputs:
                value = var.get().strip()
                if value:
                    values[label] = float(value)
            
            # Calculate based on target
            result = None
            
            # New calculations for d, m, v
            if target == 'd':
                result = values['m'] / values['v']
            elif target == 'v':
                result = values['m'] / values['d']
            elif target == 'm' and 'd' in values and 'v' in values:
                result = values['d'] * values['v']
            elif target == 'T':
                if 'm' in values:
                    m = values['m']
                else:
                    m = values['d'] * values['v']
                result = ((values['W'] * values['F']) / (m * values['S*'])) * 100
            elif target == 'W':
                if self.method_var.get() == "1":
                    if 'm' in values:
                        m = values['m']
                    else:
                        m = values['d'] * values['v']
                    result = (values['T'] * m * values['S*']) / (values['F'] * 100)
                else:
                    W_squared = ((values['a']**2 + values['b']**2) / values['L']) - values['f']
                    result = W_squared ** 0.5 if W_squared >= 0 else "Error: Negative square root"
            elif target == 'F':
                if 'm' in values:
                    m = values['m']
                else:
                    m = values['d'] * values['v']
                result = (values['T'] * m * values['S*']) / (values['W'] * 100)
            elif target == 'S*':
                if 'm' in values:
                    m = values['m']
                else:
                    m = values['d'] * values['v']
                result = (values['W'] * values['F']) / (values['T'] * m / 100)
            elif target == 'S':
                o = int(abs(values['C2'] - values['C1'])) / 10
                result = values['S*'] / (2 ** int(o))
            elif target == 'C1':
                result = values['C2'] - int(abs(values['o'] * 10))
            elif target == 'C2':
                result = values['C1'] + int(abs(values['o'] * 10))
            
            # Display result
            if isinstance(result, (int, float)):
                self.result_var.set(f"{target} = {result:.4f}")
            else:
                self.result_var.set(f"{target} = {result}")
                
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers for all fields")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = EquationSolverGUI(root)
    root.mainloop()