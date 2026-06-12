const fs = require('fs');

async function check() {
  const dummyDataContent = fs.readFileSync('./src/data/dummyData.js', 'utf8');
  console.log("dummyData.js length:", dummyDataContent.length);
  
  // Let's dynamically import using the current file path
  const dummyData = await import('./src/data/dummyData.js?t=' + Date.now());
  console.log("fmsData length:", dummyData.fmsData.length);
  
  const pending = dummyData.fmsData.filter(r => r.hasPendingCallTracker);
  console.log("Pending call trackers in dummyData:", pending.length);
}

check().catch(console.error);
