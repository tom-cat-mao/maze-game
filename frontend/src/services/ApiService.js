import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  generateMaze(size) {
    return apiClient.post('/maze/generate', { size });
  },
  solveDp(maze) {
    return apiClient.post('/solve/dp', { maze });
  },
  solveGreedy(maze) {
    return apiClient.post('/solve/greedy', { maze });
  },
  solvePuzzle(constraints) {
    return apiClient.post('/solve/puzzle', { constraints });
  },
  solveBossBattle(bossHp, skills) {
    return apiClient.post('/solve/boss', { boss_hp: bossHp, skills });
  },
};
