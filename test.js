import { fmsData } from './src/data/dummyData.js';
import { mockApi } from './src/services/mockApi.js';

console.log("fmsData length:", fmsData.length);
console.log("items with hasPendingCallTracker:", fmsData.filter(r => r.hasPendingCallTracker).length);

const test = async () => {
    const data = await mockApi.fetchCallTrackers({ username: "admin" }, () => true);
    console.log("fetchCallTrackers pending length:", data.pending.length);
};

test();
