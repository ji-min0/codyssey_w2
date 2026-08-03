import json
import os

from quiz import Quiz
from quiz_data import get_default_quizzes

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
YELLOW_BOLD = "\033[1;33m"
RESET = "\033[0m"


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

    def get_text_input(self, prompt):
        while True:
            text = input(prompt).strip()
            if not text:
                print("[안내] 입력이 없습니다. 다시 입력해주세요.\n")
                continue
            return text

    def get_answer_choice(self, prompt="정답 입력: "):
        while True:
            raw = input(prompt).strip()

            if not raw:
                print("[안내] 입력이 없습니다. 1-4 사이의 숫자를 입력하세요.\n")
                continue

            if not raw.isdigit():
                print("[안내] 잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.\n")
                continue

            answer = int(raw)
            if answer < 1 or answer > 4:
                print("[안내] 잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.\n")
                continue

            return answer

    def play_quiz(self):
        if not self.quizzes:
            print("\n[안내] 등록된 퀴즈가 없습니다.\n")
            return

        total = len(self.quizzes)
        print(f"\n[시작] 퀴즈를 시작합니다! (총 {total}문제)\n")

        correct_count = 0
        for index, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            quiz.display(index)
            print()
            answer = self.get_answer_choice()
            if quiz.is_correct(answer):
                print(f"\n{GREEN}[정답] 정답입니다.{RESET}\n")
                correct_count += 1
            else:
                print(f"\n{RED}[땡] 정답은 {quiz.answer}번입니다.{RESET}\n")

        score = round(correct_count / total * 100)
        print("=" * 40)
        print(f"{CYAN}[결과] {score}점 - {total}문제 중 {correct_count}문제 정답{RESET}")

        if score > self.best_score:
            self.best_score = score
            print(f"\n{YELLOW_BOLD}[현재 최고점] 새로운 최고 점수를 달성했습니다.{RESET}")
            self.save_state()

    def add_quiz(self):
        print("\n[퀴즈 추가]\n")

        question = self.get_text_input("문제를 입력하세요: ")
        choices = [self.get_text_input(f"선택지 {i}: ") for i in range(1, 5)]
        answer = self.get_answer_choice("정답 번호 (1-4): ")

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("\n[퀴즈가 추가되었습니다.]\n")

    def show_quiz_list(self):
        if not self.quizzes:
            print("\n[안내] 등록된 퀴즈가 없습니다.\n")
            return

        print(f"\n[퀴즈 목록] 총 {len(self.quizzes)}개의 문제가 등록되어 있습니다.\n")
        print("-" * 40)
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")
        print("-" * 40 + "\n")

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
