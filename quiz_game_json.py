import tkinter as tk
from tkinter import messagebox
import json
import random

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("English Quiz Game")
        self.root.geometry("650x550")
        self.root.configure(bg='#2c3e50')
        
        # متغیرهای بازی
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.lives = 3
        self.selected_answer = tk.StringVar()
        
        # لود کردن سوالات از فایل JSON
        self.load_questions()
        
        # شافل کردن سوالات
        random.shuffle(self.questions)
        
        # ساخت رابط کاربری
        self.setup_ui()
        
        # شروع بازی
        self.display_question()
    
    def load_questions(self):
        """بارگذاری سوالات از فایل JSON"""
        try:
            with open('english_questions.json', 'r', encoding='utf-8') as file:
                self.questions = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "english_questions.json file not found!\nPlease place the file in the project directory.")
            self.root.quit()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format!\nPlease check the file structure.")
            self.root.quit()
        
        # بررسی خالی نبودن فایل
        if not self.questions:
            messagebox.showerror("Error", "JSON file is empty!\nPlease add questions to the file.")
            self.root.quit()
    
    def setup_ui(self):
        """راه‌اندازی رابط کاربری"""
        # فریم بالایی برای اطلاعات بازی
        top_frame = tk.Frame(self.root, bg='#34495e', height=80)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        # لیبل امتیاز
        self.score_label = tk.Label(top_frame, text=f"Score: {self.score}", 
                                   font=('Arial', 14, 'bold'), bg='#34495e', fg='white')
        self.score_label.pack(side='left', padx=20, pady=20)
        
        # لیبل جان‌ها
        self.lives_label = tk.Label(top_frame, text=f"❤️ Lives: {self.lives}", 
                                   font=('Arial', 14, 'bold'), bg='#34495e', fg='red')
        self.lives_label.pack(side='right', padx=20, pady=20)
        
        # فریم وسط برای سوال و گزینه‌ها
        center_frame = tk.Frame(self.root, bg='#ecf0f1')
        center_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # لیبل سوال
        self.question_label = tk.Label(center_frame, text="", 
                                      font=('Arial', 16, 'bold'), 
                                      bg='#ecf0f1', fg='#2c3e50', wraplength=550)
        self.question_label.pack(pady=30)
        
        # دکمه‌های رادیویی برای گزینه‌ها
        self.options_frame = tk.Frame(center_frame, bg='#ecf0f1')
        self.options_frame.pack(pady=20)
        
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.options_frame, text="", variable=self.selected_answer, 
                               value=i, font=('Arial', 12), bg='#ecf0f1', 
                               anchor='w', justify='left', wraplength=550)
            rb.pack(fill='x', padx=20, pady=8)
            self.radio_buttons.append(rb)
        
        # فریم پایین برای دکمه‌ها
        bottom_frame = tk.Frame(self.root, bg='#2c3e50')
        bottom_frame.pack(fill='x', padx=10, pady=10)
        
        # دکمه ثبت پاسخ
        self.submit_btn = tk.Button(bottom_frame, text="Submit Answer", command=self.check_answer,
                                   font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                                   padx=20, pady=10, cursor='hand2')
        self.submit_btn.pack(pady=10)
        
        # دکمه خروج
        self.exit_btn = tk.Button(bottom_frame, text="Exit Game", command=self.confirm_exit,
                                 font=('Arial', 10), bg='#e74c3c', fg='white',
                                 padx=15, pady=5, cursor='hand2')
        self.exit_btn.pack(pady=5)
    
    def display_question(self):
        """نمایش سوال فعلی"""
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.config(text=f"Question {self.current_question + 1}/{len(self.questions)}: {question_data['question']}")
            
            # نمایش گزینه‌ها
            for i, option in enumerate(question_data['options']):
                self.radio_buttons[i].config(text=f"{chr(65+i)}. {option}", value=i)
            
            # پاک کردن انتخاب قبلی
            self.selected_answer.set(None)
        else:
            self.end_game()
    
    def check_answer(self):
        """بررسی پاسخ کاربر"""
        if self.selected_answer.get() == "":
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        
        selected = int(self.selected_answer.get())
        correct = self.questions[self.current_question]['correct']
        
        if selected == correct:
            self.score += 10
            messagebox.showinfo("Correct!", "✅ Excellent! +10 points")
        else:
            self.lives -= 1
            correct_answer = chr(65 + correct)
            correct_text = self.questions[self.current_question]['options'][correct]
            messagebox.showerror("Wrong!", f"❌ Sorry, that's incorrect!\nCorrect answer: {correct_answer}. {correct_text}")
            
            if self.lives == 0:
                self.end_game()
                return
        
        # به‌روزرسانی نمایش امتیاز و جان‌ها
        self.score_label.config(text=f"Score: {self.score}")
        self.lives_label.config(text=f"❤️ Lives: {self.lives}")
        
        # رفتن به سوال بعدی
        self.current_question += 1
        self.display_question()
    
    def end_game(self):
        """پایان بازی و نمایش نتیجه"""
        total_questions = len(self.questions)
        max_score = total_questions * 10
        percentage = (self.score / max_score) * 100
        
        message = f"🎮 Game Over! 🎮\n\n"
        message += f"Final Score: {self.score} out of {max_score}\n"
        message += f"Success Rate: {percentage:.1f}%\n"
        message += f"Correct Answers: {self.score // 10}\n"
        message += f"Wrong Answers: {total_questions - (self.score // 10)}\n\n"
        
        if percentage >= 80:
            message += "🏆 Excellent! You're an English master! 🏆\n"
            message += "Keep up the great work!"
        elif percentage >= 60:
            message += "👍 Good job! You have a solid foundation! 👍\n"
            message += "A little more practice and you'll be perfect!"
        elif percentage >= 40:
            message += "📚 Not bad! Keep studying and you'll improve! 📚\n"
            message += "Review the questions you missed."
        else:
            message += "💪 Don't give up! English takes practice! 💪\n"
            message += "Try again and you'll do better!"
        
        if messagebox.askyesno("Game Over", message + "\n\nWould you like to play again?"):
            self.reset_game()
        else:
            self.root.quit()
    
    def reset_game(self):
        """بازنشانی بازی"""
        self.current_question = 0
        self.score = 0
        self.lives = 3
        self.selected_answer.set(None)
        
        # شافل کردن مجدد سوالات
        random.shuffle(self.questions)
        
        # به‌روزرسانی رابط کاربری
        self.score_label.config(text=f"Score: {self.score}")
        self.lives_label.config(text=f"❤️ Lives: {self.lives}")
        
        # شروع دوباره
        self.display_question()
    
    def confirm_exit(self):
        """تأیید خروج از بازی"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit the game?"):
            self.root.quit()

if __name__ == "__main__":
    # اجرای بازی
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()