import pytest
from load_scores import load_scores
from helpers import 쓰기

# 정상 ①: 평범한 파일 읽기 (scores.csv에는 유효 5줄, 무효 5줄이 들어 있음)
def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5
    assert len(skipped) == 5

# 정상 ②: 빈 줄이 섞였을 때 무시하는지 확인
def test_빈줄은_건너뛴다():
    with open("임시.csv", "w", encoding="utf-8") as f:
        f.write("name,score\n김철수,90\n\n이영희,80\n")
    kept, skipped = load_scores("임시.csv")
    assert len(kept) == 2
    assert len(skipped) == 0

# 정상 ③: 이름에 쉼표가 따옴표로 묶여 있을 때 한 덩어리로 읽는지 확인
def test_이름에_쉼표가_있어도_읽는다():
    with open("임시.csv", "w", encoding="utf-8") as f:
        f.write('name,score\n"김, 하나",88\n')
    kept, skipped = load_scores("임시.csv")
    assert kept == [("김, 하나", 88)]
    assert len(skipped) == 0

# 예외 ①: 없는 파일을 주면 FileNotFoundError 발생
def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")

# 예외 ②: 헤더만 있는 파일을 주면 빈 리스트 반환
def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []

# 경계 ①②③: -1, 0, 1, 99, 100, 101 경계값 테스트
@pytest.mark.parametrize("점수, 유효한가", [
    (-1, False),
    (0, True),
    (1, True),
    (99, True),
    (100, True),
    (101, False),
])
def test_점수_경계값(점수, 유효한가):
    쓰기("임시.csv", 점수)
    kept, skipped = load_scores("임시.csv")
    assert (len(kept) == 1) == 유효한가

# 커버리지 보완: 이름이 비어 있을 때 건너뛰는지 확인 (55-56번 줄)
def test_이름이_비어_있으면_건너뛴다():
    with open("임시.csv", "w", encoding="utf-8") as f:
        f.write("name,score\n,90\n")
    kept, skipped = load_scores("임시.csv")
    assert len(kept) == 0
    assert len(skipped) == 1