interface RisksOpportunitiesProps {
  risks: string[];
  opportunities: string[];
}

export default function RisksOpportunities({ risks, opportunities }: RisksOpportunitiesProps) {
  return (
    <div className="space-y-6">
      {/* Risks Section */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Major Risks</h2>
        <ul className="space-y-3">
          {risks.map((risk, index) => (
            <li key={index} className="flex items-start">
              <span className="flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-full bg-red-100 text-red-600 font-medium mr-3">
                ⚠️
              </span>
              <span className="text-gray-700">{risk}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Opportunities Section */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Opportunities</h2>
        <ul className="space-y-3">
          {opportunities.map((opportunity, index) => (
            <li key={index} className="flex items-start">
              <span className="flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-full bg-green-100 text-green-600 font-medium mr-3">
                💡
              </span>
              <span className="text-gray-700">{opportunity}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
} 