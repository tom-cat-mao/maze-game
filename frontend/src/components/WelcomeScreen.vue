<template>
  <div class="welcome-screen">
    <h2>Welcome!</h2>
    <p>Set your maze size and start your adventure.</p>
    <div class="control-group">
      <label for="maze-size">Maze Size:</label>
      <input
        type="number"
        id="maze-size"
        :value="modelValue"
        @input="$emit('update:modelValue', parseInt($event.target.value))"
        min="5"
        max="50"
      />
    </div>
    <button @click="$emit('startGame')" class="start-game-btn">
      <span v-if="loading">Loading...</span>
      <span v-else>Start Game</span>
    </button>
  </div>
</template>

<script setup>
defineProps({
  modelValue: Number,
  loading: Boolean,
});
defineEmits(['update:modelValue', 'startGame']);
</script>

<style scoped>
.welcome-screen {
  text-align: center;
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.welcome-screen h2 {
  margin-top: 0;
}

.control-group {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.start-game-btn {
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

.start-game-btn:hover {
  background-color: #218838;
}
</style>
