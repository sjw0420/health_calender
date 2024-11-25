import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import calendar

# 사용자 데이터 저장
user_data = {
    "daily_water_intake": 0,
    "health_data": [],
    "exercise_time": None
}

# 중단 플래그
reminder_running = False
exercise_reminder_active = False

# 물 마시기 알림
def water_reminder(interval_minutes):
    global reminder_running
    reminder_running = True
    next_reminder = datetime.now() + timedelta(minutes=interval_minutes)

    user_data["daily_water_intake"] = 1  # 초기값 설정

    def show_alert():
        nonlocal next_reminder
        if not reminder_running:  # 알림이 중단되었으면 동작하지 않음
            return

        alert = tk.Toplevel(root)
        alert.title("물 마시기 알림")
        alert.attributes("-topmost", True)

        tk.Label(alert, text=f"💧 물 한 컵을 마실 시간입니다!\n오늘 마신 물: {user_data['daily_water_intake']}컵", font=("Arial", 12)).pack(pady=10)

        def confirm():
            nonlocal next_reminder
            user_data["daily_water_intake"] += 1
            next_reminder = datetime.now() + timedelta(minutes=interval_minutes)
            alert.destroy()

        tk.Button(alert, text="확인", command=confirm).pack(pady=5)

    def check_reminder():
        global reminder_running
        nonlocal next_reminder
        if not reminder_running:
            return
        current_time = datetime.now()
        if next_reminder is not None and current_time >= next_reminder:  # 알림 시간이 되었을 때만 실행
            show_alert()
            next_reminder = None  # 확인 버튼을 누를 때까지 대기
        root.after(1000, check_reminder)

    check_reminder()

# 물 마시기 알림 중단
def stop_water_reminder():
    global reminder_running
    if reminder_running:
        reminder_running = False
        messagebox.showinfo("알림 중단", "💧 물 마시기 알림이 중단되었습니다.")
    else:
        messagebox.showinfo("알림 중단", "현재 실행 중인 알림이 없습니다.")

# 알림 주기 설정
def set_water_reminder():
    def start_reminder():
        try:
            interval = int(interval_entry.get())
            if interval <= 0:
                raise ValueError
            reminder_window.destroy()
            messagebox.showinfo("알림 시작", f"💧 물 마시기 알림이 {interval}분 간격으로 시작됩니다.")
            water_reminder(interval)
        except ValueError:
            messagebox.showerror("입력 오류", "유효한 양의 정수를 입력하세요.")

    reminder_window = tk.Toplevel(root)
    reminder_window.title("물 마시기 알림 설정")

    tk.Label(reminder_window, text="알림 주기를 분 단위로 입력하세요:").pack(pady=10)
    interval_entry = tk.Entry(reminder_window)
    interval_entry.pack(pady=5)

    tk.Button(reminder_window, text="알림 시작", command=start_reminder).pack(pady=10)

# 건강 팁
def health_tips():
    tips_window = tk.Toplevel(root)
    tips_window.title("건강 팁")

    tk.Label(tips_window, text="📋 건강 팁", font=("Arial", 16)).pack(pady=10)
    tips = [
        "🌟 균형 잡힌 식사를 하세요!",
        "🌟 하루 30분 이상 유산소 운동을 해보세요!",
        "🌟 자기 전 1시간 전에 스크린 시간을 줄이세요.",
        "🌟 충분한 수면을 취하세요! (7-8시간 권장)",
        "🌟 물을 마실 때마다 눈의 피로를 풀어주세요."
    ]
    for tip in tips:
        tk.Label(tips_window, text=tip, font=("Arial", 12), anchor="w").pack(padx=10, pady=2)

# 신체 데이터 기록
def record_health_data():
    def save_data():
        try:
            height = float(height_entry.get())
            weight = float(weight_entry.get())
            record_date = datetime.now().strftime("%Y-%m-%d")
            user_data["health_data"].append({
                "date": record_date,
                "height": height,
                "weight": weight
            })
            messagebox.showinfo("신체 데이터 기록", f"{record_date}의 신체 데이터가 기록되었습니다!")
            record_window.destroy()
        except ValueError:
            messagebox.showerror("입력 오류", "유효한 숫자를 입력하세요.")

    record_window = tk.Toplevel(root)
    record_window.title("신체 데이터 기록")

    tk.Label(record_window, text="키 (cm):").pack(pady=5)
    height_entry = tk.Entry(record_window)
    height_entry.pack(pady=5)

    tk.Label(record_window, text="몸무게 (kg):").pack(pady=5)
    weight_entry = tk.Entry(record_window)
    weight_entry.pack(pady=5)

    tk.Button(record_window, text="기록 저장", command=save_data).pack(pady=10)

# 신체 데이터 열람
def view_health_data():
    view_window = tk.Toplevel(root)
    view_window.title("신체 데이터 열람")

    if not user_data["health_data"]:
        tk.Label(view_window, text="기록된 데이터가 없습니다.", font=("Arial", 12)).pack(pady=10)
        return

    table = ttk.Treeview(view_window, columns=("date", "height", "weight", "bmi"), show="headings")
    table.heading("date", text="날짜")
    table.heading("height", text="키 (cm)")
    table.heading("weight", text="몸무게 (kg)")
    table.heading("bmi", text="BMI")

    # 데이터 삽입
    for record in sorted(user_data["health_data"], key=lambda x: x["date"], reverse=True):
        bmi = round(record["weight"] / ((record["height"] / 100) ** 2), 2)  # BMI 계산
        table.insert("", "end", values=(record["date"], record["height"], record["weight"], bmi))

    table.pack(fill="both", expand=True, padx=10, pady=10)

# 캘린더와 데이터를 함께 표시
def view_health_calendar():
    def display_calendar(year, month):
        cal_text = calendar.TextCalendar().formatmonth(year, month)
        cal_display.delete("1.0", tk.END)
        cal_display.insert(tk.END, cal_text)

    def update_selected_data(selected_date):
        display_area.delete("1.0", tk.END)
        records = [record for record in user_data["health_data"] if record["date"] == selected_date]
        if records:
            for record in records:
                display_area.insert(tk.END, f"날짜: {record['date']}\n")
                display_area.insert(tk.END, f"키: {record['height']} cm\n")
                display_area.insert(tk.END, f"몸무게: {record['weight']} kg\n")
                bmi = round(record["weight"] / ((record["height"] / 100) ** 2), 2)
                display_area.insert(tk.END, f"BMI: {bmi}\n\n")
        else:
            display_area.insert(tk.END, "선택한 날짜에 기록된 데이터가 없습니다.")

    calendar_window = tk.Toplevel(root)
    calendar_window.title("신체 데이터 캘린더 보기")

    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    cal_display = tk.Text(calendar_window, width=25, height=10, font=("Courier", 12))
    cal_display.pack(pady=10)

    date_dropdown = tk.Listbox(calendar_window, height=5)
    date_dropdown.pack(pady=5)
    recorded_dates = sorted(set(record["date"] for record in user_data["health_data"]))
    for date in recorded_dates:
        date_dropdown.insert(tk.END, date)

    def prev_month():
        nonlocal current_year, current_month
        if current_month == 1:
            current_month = 12
            current_year -= 1
        else:
            current_month -= 1
        display_calendar(current_year, current_month)

    def next_month():
        nonlocal current_year, current_month
        if current_month == 12:
            current_month = 1
            current_year += 1
        else:
            current_month += 1
        display_calendar(current_year, current_month)

    display_calendar(current_year, current_month)

    button_frame = tk.Frame(calendar_window)
    button_frame.pack()

    tk.Button(button_frame, text="이전 달", command=prev_month).pack(side="left", padx=5)
    tk.Button(button_frame, text="다음 달", command=next_month).pack(side="left", padx=5)

    date_dropdown.bind("<<ListboxSelect>>", lambda e: update_selected_data(date_dropdown.get(tk.ACTIVE)))

    display_area = tk.Text(calendar_window, width=50, height=10, font=("Arial", 10))
    display_area.pack(pady=10)

# 운동시간 설정
def set_exercise_time():
    def save_exercise_time():
        try:
            time_input = exercise_time_entry.get()
            exercise_time = datetime.strptime(time_input, "%H:%M").time()
            user_data["exercise_time"] = exercise_time
            messagebox.showinfo("운동시간 설정", f"운동 시간이 {time_input}으로 설정되었습니다!")
            exercise_window.destroy()
            start_exercise_reminder()
        except ValueError:
            messagebox.showerror("입력 오류", "시간 형식은 HH:MM이어야 합니다.")

    exercise_window = tk.Toplevel(root)
    exercise_window.title("운동시간 설정")

    tk.Label(exercise_window, text="운동 시간을 설정하세요 (HH:MM):").pack(pady=10)
    exercise_time_entry = tk.Entry(exercise_window)
    exercise_time_entry.pack(pady=5)

    tk.Button(exercise_window, text="저장", command=save_exercise_time).pack(pady=10)

# 운동 알림
def start_exercise_reminder():
    def check_exercise_time():
        global exercise_reminder_active
        if not exercise_reminder_active or user_data["exercise_time"] is None:
            return
        now = datetime.now().time()
        exercise_time = user_data["exercise_time"]
        if now.hour == exercise_time.hour and now.minute == exercise_time.minute:
            show_exercise_alert()

        root.after(1000, check_exercise_time)

    def show_exercise_alert():
        global exercise_reminder_active
        exercise_reminder_active = False
        alert = tk.Toplevel(root)
        alert.title("운동 알림")
        alert.attributes("-topmost", True)

        tk.Label(alert, text="운동할 시간입니다!", font=("Arial", 16)).pack(pady=10)
        tk.Button(alert, text="확인", command=alert.destroy).pack(pady=10)

    global exercise_reminder_active
    exercise_reminder_active = True
    check_exercise_time()

# 메인 UI
root = tk.Tk()
root.title("건강 관리 통합 캘린더")

# 윗줄 버튼들
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Button(top_frame, text="물 마시기 알림 설정", command=set_water_reminder, width=25).pack(side="left", padx=5)
tk.Button(top_frame, text="운동시간 설정", command=set_exercise_time, width=25).pack(side="left", padx=5)
tk.Button(top_frame, text="신체 데이터 기록", command=record_health_data, width=25).pack(side="left", padx=5)

# 아랫줄 버튼들
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

tk.Button(bottom_frame, text="물 마시기 알림 중단", command=stop_water_reminder, width=25).pack(side="left", padx=5)
tk.Button(bottom_frame, text="건강 팁 보기", command=health_tips, width=25).pack(side="left", padx=5)
tk.Button(bottom_frame, text="신체 데이터 열람", command=view_health_data, width=25).pack(side="left", padx=5)
tk.Button(bottom_frame, text="캘린더 보기", command=view_health_calendar, width=25).pack(side="left", padx=5)

# 종료 버튼
tk.Button(root, text="종료", command=root.quit, width=25).pack(pady=10)

root.mainloop()
