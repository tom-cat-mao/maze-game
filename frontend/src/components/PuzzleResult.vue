<template>
  <div>
    <h3>Puzzle Solved!</h3>
    <div class="puzzle-password-container">
      <span>Password:</span>
      <span v-for="(digit, index) in solution" :key="index" class="password-digit">
        {{ digit }}
      </span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  solution: Array,
});
</script>

<style scoped>
.puzzle-password-container {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.password-digit {
  display: inline-block;
  width: 30px;
  height: 30px;
  line-height: 30px;
  text-align: center;
  font-weight: bold;
  border: 1px solid #ced4da;
  background-color: #e9ecef;
  border-radius: 4px;
  font-family: 'Courier New', Courier, monospace;
}
</style>
