# jump_game_genetic_algorithm

레벨 1,2,3,4,5의 벽을 점프 또는 웅크리기로 벽과의 충돌을 피하는 게임

inputs
1. 벽의 레벨 * 0.25 
2. 첫 번째로 다가오는 벽의 위치 

outputs
 1. [1, 0, 0] : 가만히 
 2. [0, 1, 0] : 웅크리기
 3. [0, 0, 1] : 점프

처음 테스트는 50개의 점퍼들로 진행 했지만 100번 이상 진화를 거쳐도 2번 벽과 계속 충돌함  


빠른 테스트를 위해 점퍼들을 100개로 늘렸고 hidden layer를 한층 더 쌓음  

-첫 번째 테스트  
296번째 진화 때 점퍼가 계속해서 살아남아서 게임을 종료함.  


-두 번째 테스트  
12번째 진화 때 점퍼가 계속해서 살아남아서 게임을 종료함.  


youtube https://www.youtube.com/watch?v=DPfLMHV4qyE  
velog https://velog.io/@zz121210/%EC%A0%90%ED%94%84-%EA%B2%8C%EC%9E%84-%EC%9C%A0%EC%A0%84-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98Gentic-algorithm
