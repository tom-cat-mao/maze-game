<template>
  <div class="battle-report">
    <h3>Boss Battle Report</h3>
    <div class="vs-container">
      <div class="vs-panel">
        <strong>Your Skills</strong>
        <div v-if="playerSkills" class="vs-items">
          <span v-for="skill in playerSkills" :key="skill.name" class="skill-badge player">
            {{ skill.name }} (DMG: {{ skill.damage }})
          </span>
        </div>
      </div>
      <div class="vs-separator">VS</div>
      <div class="vs-panel">
        <strong>Enemy Lineup</strong>
        <div v-if="bossHps" class="vs-items">
          <span v-for="(hp, index) in bossHps" :key="index" class="skill-badge enemy">
            BOSS ({{ hp }} HP)
          </span>
        </div>
      </div>
    </div>
    <div class="battle-log">
      <strong>Optimal Sequence:</strong>
      <ul class="log-list">
        <li v-for="(skill, index) in battleResult.sequence" :key="index">
          Turn {{ index + 1 }}: Used <strong>{{ skill }}</strong>
        </li>
      </ul>
    </div>
    <div class="battle-summary">
      <strong>Total Turns to Win: <span class="value-player">{{ battleResult.turns }}</span></strong>
    </div>
  </div>
</template>

<script setup>
defineProps({
  playerSkills: Array,
  bossHps: Array,
  battleResult: Object,
});
</script>

<style scoped>
.battle-report h3 {
  margin-top: 0;
  border-bottom: 2px solid #dc3545;
  padding-bottom: 5px;
  margin-bottom: 15px;
  text-align: center;
}

.vs-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  text-align: center;
  margin-bottom: 15px;
}

.vs-panel {
  flex: 1;
}

.vs-items {
  margin-top: 5px;
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  justify-content: center;
}

.vs-separator {
  font-size: 2em;
  color: #dc3545;
  font-weight: bold;
  padding: 0 10px;
}

.battle-log {
  margin-top: 15px;
}

.log-list {
  list-style-type: none;
  padding-left: 0;
  font-family: 'Courier New', Courier, monospace;
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 10px;
  margin-top: 5px;
  max-height: 150px;
  overflow-y: auto;
  border: 1px solid #e9ecef;
}

.log-list li {
  padding: 2px 0;
}

.battle-summary {
  text-align: right;
  margin-top: 10px;
  font-weight: bold;
}

.skill-badge {
  color: white;
  padding: 4px 10px;
  border-radius: 15px;
  font-size: 0.9em;
  margin: 2px;
}

.skill-badge.player {
  background-color: #007bff;
}

.skill-badge.enemy {
  background-color: #6f42c1;
}

.value-player {
    color: #28a745;
    font-weight: bold;
}
</style>
