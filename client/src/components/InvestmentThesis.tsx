interface InvestmentThesisProps {
  thesis: string[];
}

export default function InvestmentThesis({ thesis }: InvestmentThesisProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Investment Thesis</h2>
      
      <ul className="space-y-3">
        {thesis.map((point, index) => (
          <li key={index} className="flex items-start">
            <span className="flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-full bg-blue-100 text-blue-600 font-medium mr-3">
              {index + 1}
            </span>
            <span className="text-gray-700">{point}</span>
          </li>
        ))}
      </ul>
    </div>
  );
} 