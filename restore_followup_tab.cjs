const fs = require('fs');
const path = require('path');

const filepath = path.join('c:', 'Users', 'prata', 'Downloads', 'LeadToEnquiry', 'src', 'pages', 'FollowUp', 'FollowUp.jsx');
let content = fs.readFileSync(filepath, 'utf8');

const badChunkRegex = /      matchesCompanyFilter &&\r?\n      searchTerm === "" \|\|/;

const restoredChunk = `      matchesCompanyFilter &&
      matchesPersonFilter &&
      matchesPhoneFilter
    )
  })

  useEffect(() => {
    // Reset specific filters when switching tabs
    if (activeTab !== "pending") {
      setCompanyFilter([])
      setPersonFilter([])
      setPhoneFilter([])
    }
  }, [activeTab])

  const filteredHistoryFollowUps = historyFollowUps.filter((followUp) => {
    const searchLower = searchTerm.toLowerCase()
    const matchesSearch =
      searchTerm === "" ||`;

content = content.replace(badChunkRegex, restoredChunk);

fs.writeFileSync(filepath, content);
console.log('FollowUp.jsx restored!');
