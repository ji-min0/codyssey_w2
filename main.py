import json
import os

from quiz import Quiz
from quiz_data import get_default_quizzes

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.load_state()

    def load_state(self):
        if not os.path.exists(STATE_FILE):
            self.quizzes = get_default_quizzes()
            self.best_score = 0
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            self.best_score = data["best_score"]
            print(
                f"[안내] 저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)\n"
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("[안내] 저장된 데이터가 손상되어 기본 퀴즈 데이터로 초기화합니다.\n")
            self.quizzes = get_default_quizzes()
            self.best_score = 0

    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError:
            print("[안내] 데이터 저장 중 오류가 발생했습니다.\n")

    def show_menu(self):
        print("=" * 40)
        print(" " * 13 + "Quiz Game Menu")
        print("=" * 40)
        print(" 1  퀴즈 풀기")
        print(" 2  퀴즈 추가")
        print(" 3  퀴즈 목록")
        print(" 4  점수 확인")
        print(" 5  종료")
        print("=" * 40)

    def get_menu_choice(self):
        while True:
            try:
                raw = input("선택: ").strip()
            except (EOFError, KeyboardInterrupt):
                return 5

            if not raw:
                print("[안내] 입력이 없습니다. 1-5 사이의 숫자를 입력하세요.\n")
                continue

            if not raw.isdigit():
                print("[안내] 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.\n")
                continue

            choice = int(raw)
            if choice < 1 or choice > 5:
                print("[안내] 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.\n")
                continue

            return choice

    def play_quiz(self):
        print("\n[퀴즈 풀기 기능은 준비 중입니다.]\n")

    def add_quiz(self):
        print("\n[퀴즈 추가 기능은 준비 중입니다.]\n")

    def show_quiz_list(self):
        print("\n[퀴즈 목록 기능은 준비 중입니다.]\n")

    def show_score(self):
        print("\n[점수 확인 기능은 준비 중입니다.]\n")

    def run(self):
        while True:
            self.show_menu()
            choice = self.get_menu_choice()

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                self.save_state()
                print("\n[ 게임 종료 ]")
                break


def main():
    game = QuizGame()
    try:
        game.run()
    except (EOFError, KeyboardInterrupt):
        game.save_state()
        print("\n[ 게임 종료 ]")


if __name__ == "__main__":
    main()
