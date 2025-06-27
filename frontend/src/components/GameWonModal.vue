<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2>Congratulations!</h2>
      <p class="final-score-label">Your Final Score</p>
      <p class="final-score-value">{{ score }}</p>
      <button @click="$emit('playAgain')" class="play-again-btn">Play Again</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  score: Number,
});
defineEmits(['playAgain']);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px 40px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  animation: fadeIn 0.3s ease-out;
}

.modal-content h2 {
  color: #007bff;
  margin-top: 0;
}

.final-score-label {
  font-size: 1.2em;
  color: #6c757d;
  margin-bottom: 5px;
}

.final-score-value {
  font-size: 3em;
  font-weight: bold;
  color: #ffc107;
  margin-top: 0;
}

.play-again-btn {
  padding: 12px 25px;
  font-size: 1.1em;
  margin-top: 20px;
  background-color: #28a745;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.play-again-btn:hover {
  background-color: #218838;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
