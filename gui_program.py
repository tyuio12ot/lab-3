import tkinter as tk
from tkinter import ttk, messagebox

class LengthConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер единиц длины")
        self.root.geometry("550x450")
        self.root.resizable(False, False)

        # Словарь коэффициентов перевода в метры (базовая единица)
        self.units_to_meters = {
            "Метры (m)": 1,
            "Сантиметры (cm)": 0.01,
            "Миллиметры (mm)": 0.001,
            "Километры (km)": 1000,
            "Дюймы (in)": 0.0254,
            "Футы (ft)": 0.3048,
            "Ярды (yd)": 0.9144,
            "Мили (mi)": 1609.34,
            "Морские мили (nmi)": 1852
        }

        # Список единиц для выпадающих списков
        self.units_list = list(self.units_to_meters.keys())

        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="Конвертер единиц длины",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        # Рамка для ввода исходных данных
        input_frame = tk.LabelFrame(self.root, text="Исходные данные", padx=10, pady=10)
        input_frame.pack(padx=20, pady=10, fill="x")
        tk.Label(input_frame, text="Введите число:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_value = tk.Entry(input_frame, width=25, font=("Arial", 12))
        self.entry_value.grid(row=0, column=1, padx=5, pady=5)
        self.entry_value.insert(0, "1")  # Пример значения
        tk.Label(input_frame, text="Исходная единица:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.from_unit = ttk.Combobox(input_frame, values=self.units_list, width=22, state="readonly")
        self.from_unit.grid(row=1, column=1, padx=5, pady=5)
        self.from_unit.current(0)  # Выбираем "Метры" по умолчанию
        # Рамка для целевых данных
        target_frame = tk.LabelFrame(self.root, text="Целевые данные", padx=10, pady=10)
        target_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(target_frame, text="Целевая единица:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.to_unit = ttk.Combobox(target_frame, values=self.units_list, width=22, state="readonly")
        self.to_unit.grid(row=0, column=1, padx=5, pady=5)
        self.to_unit.current(1)  # Выбираем "Сантиметры" по умолчанию

        # Кнопка конвертации
        self.convert_button = tk.Button(
            self.root,
            text="Конвертировать",
            command=self.convert,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.convert_button.pack(pady=15)

        # Рамка для результата
        result_frame = tk.LabelFrame(self.root, text="Результат конвертации", padx=10, pady=15)
        result_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Основной результат - крупным шрифтом
        self.result_label = tk.Label(
            result_frame,
            text="Введите данные и нажмите 'Конвертировать'",
            font=("Arial", 14, "bold"),
            fg="blue",
            wraplength=450,
            justify="center"
        )
        self.result_label.pack(expand=True, fill="both")

        # Дополнительная информация для отладки
        self.debug_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 9),
            fg="gray"
        )
        self.debug_label.pack(side="bottom", pady=5)

        # Информация о программе
        info_label = tk.Label(
            self.root,
            text="Поддерживаемые единицы: метры, сантиметры, миллиметры, километры,\n"
                 "дюймы, футы, ярды, мили, морские мили",
            font=("Arial", 8),
            fg="gray"
        )
        info_label.pack(side="bottom", pady=5)

    def convert(self):
        """Основная функция конвертации с обработкой ошибок"""
        try:
            # Показываем, что процесс начался
            self.debug_label.config(text="Выполняется конвертация...")
            self.result_label.config(text="Вычисляется...", fg="orange")
            self.root.update()  # Обновляем интерфейс

            # Получаем и проверяем ввод числа
            value_str = self.entry_value.get().strip()

            if not value_str:
                raise ValueError("Поле ввода не может быть пустым")

            # Заменяем запятую на точку для корректного преобразования
            value_str = value_str.replace(',', '.')
            value = float(value_str)

            # Получаем выбранные единицы
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()

            if not from_unit or not to_unit:
                raise ValueError("Пожалуйста, выберите исходную и целевую единицы измерения")

            # Конвертация в метры
            value_in_meters = value * self.units_to_meters[from_unit]

            # Конвертация из метров в целевую единицу
            result = value_in_meters / self.units_to_meters[to_unit]

            # Форматирование результата
            if abs(result) < 0.0001 or abs(result) > 1000000:
                result_text = f"{value} {from_unit} = {result:.6e} {to_unit}"
            else:
                # Округляем до 6 знаков, но убираем лишние нули
                result_rounded = round(result, 10)
                # Убираем .0 если число целое
                if result_rounded.is_integer():
                    result_display = f"{value} {from_unit} = {int(result_rounded)} {to_unit}"
                else:
                    result_display = f"{value} {from_unit} = {result_rounded:.6f} {to_unit}"
                result_text = result_display

            # Выводим результат
            self.result_label.config(text=result_text, fg="green")
            self.debug_label.config(text=f"✓ Конвертация выполнена успешно!")

            # Также выводим в консоль для отладки
            print(f"Результат: {result_text}")

        except ValueError as e:
            if "could not convert string to float" in str(e) or "invalid literal" in str(e):
                error_msg = "Ошибка: Введите корректное число\n(используйте цифры, точку или запятую)"
                messagebox.showerror("Ошибка ввода", error_msg)
                self.result_label.config(text=error_msg, fg="red")
            else:
                messagebox.showerror("Ошибка", str(e))
                self.result_label.config(text=f"Ошибка: {str(e)}", fg="red")
            self.debug_label.config(text="✗ Ошибка при конвертации")

        except KeyError as e:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите единицы измерения из списка.")
            self.result_label.config(text="Ошибка: не выбраны единицы измерения", fg="red")
            self.debug_label.config(text="✗ Ошибка: не выбраны единицы")

        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Произошла ошибка при делении.")
            self.result_label.config(text="Ошибка в расчетах", fg="red")
            self.debug_label.config(text="✗ Ошибка деления")

        except Exception as e:
            error_msg = f"Непредвиденная ошибка: {str(e)}"
            messagebox.showerror("Ошибка", error_msg)
            self.result_label.config(text=error_msg, fg="red")
            self.debug_label.config(text="✗ Непредвиденная ошибка")
            print(f"Ошибка: {str(e)}")  # Вывод в консоль для отладки

def main():
    root = tk.Tk()
    app = LengthConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
