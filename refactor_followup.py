import re
import os

filepath = r'c:\Users\prata\Downloads\LeadToEnquiry\src\pages\FollowUp\FollowUp.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports for DataTable and FollowUpFilter
if 'import DataTable from' not in content:
    content = re.sub(r'(import \{ AuthContext \} from "../../App")', r'\1\nimport DataTable from "../../components/DataTable"\nimport FollowUpFilter from "../../components/follow-up/FollowUpFilter"', content)

# Remove the old import if it existed (e.g. if we accidentally double add)

# Find the start of the return statement
return_index = content.find('  return (\n    <div className="min-h-screen')

if return_index == -1:
    print("Could not find the return statement.")
    exit(1)

# Keep everything before the return statement
before_return = content[:return_index]

# Add pagination state and rendering functions
new_logic = """
  // Pagination State
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(10);
  
  // Calculate pagination
  const currentData = activeTab === "pending" ? filteredPendingFollowUps : filteredHistoryFollowUps;
  const totalPages = Math.max(1, Math.ceil(currentData.length / itemsPerPage));
  const paginatedData = currentData.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

  // Reset page when tab or filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [activeTab, searchTerm, companyFilter, personFilter, phoneFilter, dateFilter, filterType]);

  const determinePriority = (source) => {
    if (!source) return "Low";
    const lower = source.toLowerCase();
    if (lower.includes("indiamart") || lower.includes("tradeindia")) return "Medium";
    if (lower.includes("direct") || lower.includes("website")) return "High";
    return "Low";
  };

  const formatItemQty = (itemQty) => {
    if (!itemQty) return "-";
    if (typeof itemQty === 'string') return itemQty;
    if (Array.isArray(itemQty)) {
      return itemQty.map(i => `${i.item} (${i.qty})`).join(", ");
    }
    return "-";
  };

  const getHeaders = () => {
    if (activeTab === "pending") {
      const baseHeaders = [
        "Actions", "Call Date", "Lead No.", "Company Name", "Person Name", 
        "Phone No.", "Lead Source", "Location", "Customer Say", "Enquiry Status"
      ];
      if (isAdmin()) baseHeaders.push("Assigned To");
      baseHeaders.push("Item/Qty");
      return baseHeaders;
    } else {
      return columnOptions
        .filter(opt => visibleColumns[opt.key])
        .map(opt => opt.label);
    }
  };

  const renderPendingRow = (followUp, index) => (
    <tr key={`${followUp.leadId}-${index}`} className="hover:bg-slate-50 transition-colors">
      <td className="sticky left-0 z-10 bg-white px-3 sm:px-4 py-3 sm:py-4 text-sm font-medium border-r border-gray-200">
        <div className="flex flex-col sm:flex-row space-y-1 sm:space-y-0 sm:space-x-2">
          <Link to={`/follow-up/new?leadId=${followUp.leadId}&leadNo=${followUp.leadId}`}>
            <button className="w-full sm:w-auto px-2 sm:px-3 py-1 text-xs border border-sky-200 text-sky-600 hover:bg-sky-50 rounded-md transition-colors whitespace-nowrap">
              Call Now <ArrowRightIcon className="ml-1 h-3 w-3 inline" />
            </button>
          </Link>
        </div>
      </td>
      <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.nextCallDate || followUp.timestamp}</td>
      <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm font-medium text-gray-900 whitespace-nowrap">{followUp.leadId}</td>
      <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500"><div className="max-w-[150px] truncate" title={followUp.companyName}>{followUp.companyName}</div></td>
      <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500"><div className="max-w-[120px] truncate" title={followUp.personName}>{followUp.personName}</div></td>
      <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.phoneNumber}</td>
      <td className="px-3 sm:px-4 py-3 sm:py-4">
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${followUp.priority === "High" ? "bg-red-100 text-red-800" : followUp.priority === "Medium" ? "bg-blue-100 text-blue-800" : "bg-slate-100 text-slate-800"}`}>
          {followUp.leadSource}
        </span>
      </td>
      <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500"><div className="max-w-[120px] truncate" title={followUp.location}>{followUp.location}</div></td>
      <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500"><div className="max-w-[200px] truncate" title={followUp.customerSay}>{followUp.customerSay}</div></td>
      <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500"><div className="max-w-[120px] truncate" title={followUp.enquiryStatus}>{followUp.enquiryStatus}</div></td>
      {isAdmin() && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.assignedTo}</td>}
      <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500"><div className="min-w-[200px] break-words whitespace-normal" title={formatItemQty(followUp.itemQty)}>{formatItemQty(followUp.itemQty)}</div></td>
    </tr>
  );

  const renderHistoryRow = (followUp, index) => (
    <tr key={`${followUp.leadNo}-${index}`} className="hover:bg-slate-50 transition-colors">
      {visibleColumns.timestamp && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.timestamp}</td>}
      {visibleColumns.leadNo && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.leadNo}</td>}
      {visibleColumns.companyName && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500"><div className="max-w-[150px] truncate">{followUp.companyName}</div></td>}
      {visibleColumns.customerSay && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500"><div className="max-w-[200px] truncate">{followUp.customerSay}</div></td>}
      {visibleColumns.status && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.status}</td>}
      {visibleColumns.enquiryStatus && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.enquiryReceivedStatus}</td>}
      {visibleColumns.receivedDate && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.enquiryReceivedDate}</td>}
      {visibleColumns.state && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.state}</td>}
      {visibleColumns.projectName && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500"><div className="max-w-[150px] truncate">{followUp.projectName}</div></td>}
      {visibleColumns.salesType && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.salesType}</td>}
      {visibleColumns.productDate && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.requiredProductDate}</td>}
      {visibleColumns.projectValue && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.projectApproxValue}</td>}
      {visibleColumns.item1 && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.itemName1}</td>}
      {visibleColumns.qty1 && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.itemQty1}</td>}
      {visibleColumns.item2 && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.itemName2}</td>}
      {visibleColumns.qty2 && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.itemQty2}</td>}
      {visibleColumns.item3 && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.itemName3}</td>}
      {visibleColumns.qty3 && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.itemQty3}</td>}
      {visibleColumns.item4 && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.itemName4}</td>}
      {visibleColumns.qty4 && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.itemQty4}</td>}
      {visibleColumns.item5 && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.itemName5}</td>}
      {visibleColumns.qty5 && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.itemQty5}</td>}
      {visibleColumns.nextAction && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.nextAction}</td>}
      {visibleColumns.callDate && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.nextCallDate}</td>}
      {visibleColumns.callTime && <td className="px-3 sm:px-4 py-3 sm:py-4 text-sm text-gray-500 whitespace-nowrap">{followUp.nextCallTime}</td>}
    </tr>
  );

  const renderPendingCard = (followUp, index) => (
    <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 space-y-3">
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">{followUp.leadId}</span>
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${determinePriority(followUp.leadSource) === "High" ? "bg-red-100 text-red-800" : determinePriority(followUp.leadSource) === "Medium" ? "bg-yellow-100 text-yellow-800" : "bg-green-100 text-green-800"}`}>
              {determinePriority(followUp.leadSource)} Priority
            </span>
          </div>
          <h3 className="font-bold text-gray-900 text-lg">{followUp.companyName}</h3>
          <p className="text-sm text-gray-600">{followUp.personName}</p>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-3 text-sm">
        <div>
          <p className="text-xs text-gray-500">Phone</p>
          <p className="font-medium">{followUp.phoneNumber}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500">Next Call</p>
          <p className="font-medium text-orange-600">{followUp.nextCallDate || "Not Set"}</p>
        </div>
        <div className="col-span-2">
          <p className="text-xs text-gray-500">Customer Say</p>
          <p className="text-gray-700 bg-gray-50 p-2 rounded text-xs line-clamp-2">{followUp.customerSay || "No feedback recorded"}</p>
        </div>
      </div>
      <div className="pt-2 border-t border-gray-100 flex justify-end">
        <Link to={`/follow-up/new?leadId=${followUp.leadId}&leadNo=${followUp.leadId}`} className="w-full">
          <button className="flex items-center justify-center px-4 py-2 border border-sky-600 rounded-md text-sm font-medium text-sky-600 bg-white hover:bg-sky-50 w-full">
            Call Now <ArrowRightIcon className="ml-1 h-4 w-4 inline" />
          </button>
        </Link>
      </div>
    </div>
  );

  const renderHistoryCard = (followUp, index) => (
    <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 space-y-3">
      <div className="flex justify-between items-start">
        <div>
          <span className="text-xs font-semibold text-gray-500">{followUp.timestamp}</span>
          <h3 className="font-bold text-gray-900">{followUp.companyName}</h3>
          <p className="text-xs text-blue-600 font-medium">{followUp.leadNo}</p>
        </div>
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${followUp.status === "Completed" ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"}`}>
          {followUp.status}
        </span>
      </div>
      <div className="grid grid-cols-2 gap-2 text-sm text-gray-600">
        <div><span className="block text-xs text-gray-400">Project</span><p className="truncate">{followUp.projectName}</p></div>
        <div><span className="block text-xs text-gray-400">Status</span><p>{followUp.enquiryReceivedStatus}</p></div>
        <div><span className="block text-xs text-gray-400">Sales Type</span><p>{followUp.salesType}</p></div>
        <div><span className="block text-xs text-gray-400">Value</span><p>{followUp.projectApproxValue}</p></div>
      </div>
    </div>
  );

  return (
    <div className="flex flex-col flex-1 h-full min-h-0 w-full p-1 md:p-1.5">
      <FollowUpFilter
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        companyFilter={companyFilter}
        setCompanyFilter={setCompanyFilter}
        personFilter={personFilter}
        setPersonFilter={setPersonFilter}
        phoneFilter={phoneFilter}
        setPhoneFilter={setPhoneFilter}
        dateFilter={dateFilter}
        setDateFilter={setDateFilter}
        dateFilterCounts={dateFilterCounts}
        filterType={filterType}
        setFilterType={setFilterType}
        showColumnDropdown={showColumnDropdown}
        setShowColumnDropdown={setShowColumnDropdown}
        visibleColumns={visibleColumns}
        handleSelectAll={handleSelectAll}
        handleColumnToggle={handleColumnToggle}
        columnOptions={columnOptions}
        pendingFollowUps={pendingFollowUps}
      />

      <div className="flex-1 flex flex-col min-h-0 mt-1">
        {isLoading ? (
          <div className="p-8 text-center flex-1 flex flex-col justify-center items-center bg-white rounded-lg border border-gray-200 shadow-sm">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-sky-600 mb-4"></div>
            <p className="text-slate-500">Loading follow-up data...</p>
          </div>
        ) : (
          <DataTable
            headers={getHeaders()}
            data={paginatedData}
            renderRow={activeTab === "pending" ? renderPendingRow : renderHistoryRow}
            renderCard={activeTab === "pending" ? renderPendingCard : renderHistoryCard}
            currentPage={currentPage}
            totalPages={totalPages}
            itemsPerPage={itemsPerPage}
            onPageChange={setCurrentPage}
            onItemsPerPageChange={setItemsPerPage}
            totalResults={currentData.length}
          />
        )}
      </div>
    </div>
  );
};

export default FollowUp;
"""

new_content = before_return + new_logic
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully refactored FollowUp.jsx!")
