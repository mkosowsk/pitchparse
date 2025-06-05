interface Company {
  id: number;
  name: string;
  sector: string;
  hq: string;
  revenue: string;
  growth: string;
  margin: string;
}

interface CompanyCardProps {
  company: Company;
  isSelected: boolean;
  onClick: () => void;
}

export default function CompanyCard({ company, isSelected, onClick }: CompanyCardProps) {
  return (
    <div
      className={`p-6 rounded-lg border cursor-pointer transition-all ${
        isSelected
          ? 'bg-blue-50 border-blue-500 shadow-lg'
          : 'bg-white border-gray-200 hover:border-blue-300'
      }`}
      onClick={onClick}
    >
      <h2 className="text-xl font-semibold text-gray-900 mb-4">{company.name}</h2>
      
      <div className="space-y-3">
        <div className="flex justify-between">
          <span className="text-gray-600">Sector</span>
          <span className="font-medium">{company.sector}</span>
        </div>
        
        <div className="flex justify-between">
          <span className="text-gray-600">HQ</span>
          <span className="font-medium">{company.hq}</span>
        </div>
        
        <div className="flex justify-between">
          <span className="text-gray-600">Revenue</span>
          <span className="font-medium">{company.revenue}</span>
        </div>
        
        <div className="flex justify-between">
          <span className="text-gray-600">Growth</span>
          <span className="font-medium text-green-600">{company.growth}</span>
        </div>
        
        <div className="flex justify-between">
          <span className="text-gray-600">Margin</span>
          <span className="font-medium text-green-600">{company.margin}</span>
        </div>
      </div>
    </div>
  );
} 