from random import sample

sample_classes = {
    'sentences': ["안녕하세요", "너는 음운론이 좋니?", "오빠 뭐해요?", "화용론 개 어려워", "아닙니다"],
    'consonant_clusters': ["읊지마", "밝잖니", "닭도리탕", "닭"],
    'hanja': ["不動産", "靑綠", "綠色", "年度", "音韻論", "論爭"],
    'mandatory_processes': ["각막", "법률", "범람", "한라산", "발냄새", "밥물", "햇님", "억만장자", "음운론", "화용론"],
    'optional_processes': ["한글", "신문", "반갑게"],
    'palatalization': ["굳이?", "맏이", "돋이", "해돋이", "같이", "끝이"],
    'random_words': ["툭하면", "박수", "덮밥", "통사론", "의미론", "스테로이드", "사랑", "우리", "예시", "남녀", "엉터리", "원숭이",
                     "엄준식", "왜날쀍", "개미퍼먹어", "무를주세요", "엄친아", "멘붕", "안습", "잼민이", "분가하겠습니다"]
}

weights = [1, 5, 2, 6, 5, 5, 2]


sample_pool = [item for key, weight in zip(sample_classes.keys(), weights) for item in sample_classes[key] * weight]

sample_word = sample(sample_pool, 1)[0]
