'use client';

import { useState } from 'react';
import CompanyCard from '@/components/CompanyCard';
import InvestmentThesis from '@/components/InvestmentThesis';
import RisksOpportunities from '@/components/RisksOpportunities';
import PDFUploader from '@/components/PDFUploader';

// Dummy data for companies
const companies = [
  {
    id: 1,
    name: 'TechCorp Solutions',
    sector: 'Enterprise Software',
    hq: 'San Francisco, CA',
    revenue: '$45M',
    growth: '32%',
    margin: '28%',
    investmentThesis: [
      'Leading provider of AI-powered enterprise automation solutions',
      'Strong recurring revenue model with 95% subscription base',
      'Expanding into high-growth verticals with proven product-market fit',
      'Experienced management team with successful track record',
      'Attractive valuation relative to growth metrics'
    ],
    risks: [
      'Competition from larger tech companies entering the space',
      'Dependency on key enterprise customers',
      'Need for continued R&D investment'
    ],
    opportunities: [
      'International expansion potential',
      'New product line development',
      'Strategic acquisition targets'
    ]
  },
  {
    id: 2,
    name: 'GreenEnergy Innovations',
    sector: 'Clean Energy',
    hq: 'Austin, TX',
    revenue: '$28M',
    growth: '45%',
    margin: '22%',
    investmentThesis: [
      'Pioneer in next-gen solar panel technology',
      'Strong government contracts and subsidies',
      'Scalable manufacturing process with high margins',
      'Growing demand in emerging markets',
      'Proprietary IP with multiple patents'
    ],
    risks: [
      'Regulatory changes in energy sector',
      'Raw material price volatility',
      'Capital intensive growth requirements'
    ],
    opportunities: [
      'Partnership with major utilities',
      'New market expansion',
      'Technology licensing opportunities'
    ]
  },
  {
    id: 3,
    name: 'HealthTech Dynamics',
    sector: 'Healthcare Technology',
    hq: 'Boston, MA',
    revenue: '$35M',
    growth: '38%',
    margin: '25%',
    investmentThesis: [
      'Revolutionary patient monitoring platform',
      'FDA-approved technology with strong clinical results',
      'Growing network of hospital partnerships',
      'Recurring revenue from subscription model',
      'Strong intellectual property portfolio'
    ],
    risks: [
      'Healthcare regulatory compliance',
      'Data privacy concerns',
      'Integration challenges with legacy systems'
    ],
    opportunities: [
      'International market expansion',
      'New product development',
      'Strategic healthcare partnerships'
    ]
  }
];

interface ParsedPDFData {
  sector: string;
  hq: string;
  revenue: string;
  growth: string;
  margin: string;
  chunks: string[];
}

export default function Dashboard() {
  const [selectedCompany, setSelectedCompany] = useState(companies[0]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [parsedData, setParsedData] = useState<ParsedPDFData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedChunkIndex, setSelectedChunkIndex] = useState<number | null>(null);

  const handleFileUpload = async (file: File) => {
    setIsProcessing(true);
    setError(null);
    setSelectedChunkIndex(null);
    try {
      // Create FormData
      const formData = new FormData();
      formData.append('file', file);

      // Send to backend
      const response = await fetch('/api/process-pdf', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to process PDF');
      }

      const result = await response.json();
      if (result.error) {
        throw new Error(result.error);
      }

      setParsedData(result.data);
      
      // Create a new company card with the parsed data
      const newCompany = {
        id: companies.length + 1,
        name: file.name.replace('.pdf', ''),
        sector: result.data.sector || 'Not found',
        hq: result.data.hq || 'Not found',
        revenue: result.data.revenue || 'Not found',
        growth: result.data.growth || 'Not found',
        margin: result.data.margin || 'Not found',
        investmentThesis: ['Investment thesis points will be extracted in future updates'],
        risks: ['Risks will be extracted in future updates'],
        opportunities: ['Opportunities will be extracted in future updates']
      };

      // Add the new company to the list and select it
      companies.push(newCompany);
      setSelectedCompany(newCompany);
      
    } catch (error) {
      console.error('Error processing PDF:', error);
      setError(error instanceof Error ? error.message : 'Failed to process PDF');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Investment Dashboard</h1>
        
        {/* PDF Upload Section */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Upload Company PDF</h2>
          <PDFUploader onFileUpload={handleFileUpload} />
          {isProcessing && (
            <div className="mt-4 text-center text-gray-600">
              Processing PDF... Please wait.
            </div>
          )}
          {error && (
            <div className="mt-4 text-center text-red-600">
              Error: {error}
            </div>
          )}
        </div>
        
        {/* Company Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {companies.map((company) => (
            <CompanyCard
              key={company.id}
              company={company}
              isSelected={selectedCompany.id === company.id}
              onClick={() => setSelectedCompany(company)}
            />
          ))}
        </div>

        {/* Selected Company Details */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-8">
            <InvestmentThesis thesis={selectedCompany.investmentThesis} />
          </div>
          <div className="space-y-8">
            <RisksOpportunities
              risks={selectedCompany.risks}
              opportunities={selectedCompany.opportunities}
            />
          </div>
        </div>

        {/* PDF Chunks Section */}
        {parsedData && parsedData.chunks && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">PDF Content Chunks</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Chunk Navigation */}
              <div className="bg-white rounded-lg shadow p-4">
                <h3 className="font-medium text-gray-900 mb-2">Chunks</h3>
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {parsedData.chunks.map((chunk, index) => (
                    <button
                      key={index}
                      onClick={() => setSelectedChunkIndex(index)}
                      className={`w-full text-left p-2 rounded ${
                        selectedChunkIndex === index
                          ? 'bg-blue-50 text-blue-700'
                          : 'hover:bg-gray-50'
                      }`}
                    >
                      <span className="font-medium">Chunk {index + 1}</span>
                      <p className="text-sm text-gray-600 truncate">
                        {chunk.slice(0, 100)}...
                      </p>
                    </button>
                  ))}
                </div>
              </div>

              {/* Selected Chunk Content */}
              <div className="bg-white rounded-lg shadow p-4">
                <h3 className="font-medium text-gray-900 mb-2">
                  {selectedChunkIndex !== null
                    ? `Chunk ${selectedChunkIndex + 1} Content`
                    : 'Select a chunk to view its content'}
                </h3>
                {selectedChunkIndex !== null && (
                  <div className="prose max-w-none">
                    <p className="whitespace-pre-wrap">
                      {parsedData.chunks[selectedChunkIndex]}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Extracted Company Details */}
        {parsedData && (
          <div className="mt-8">
            <h2 className="text-2xl font-bold mb-4">Extracted Company Details</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Sector</h3>
                <p className="text-gray-600 dark:text-gray-300">{parsedData.sector}</p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Headquarters</h3>
                <p className="text-gray-600 dark:text-gray-300">{parsedData.hq}</p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Revenue</h3>
                <p className="text-gray-600 dark:text-gray-300">{parsedData.revenue}</p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Growth</h3>
                <p className="text-gray-600 dark:text-gray-300">{parsedData.growth}</p>
              </div>
              <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Margin</h3>
                <p className="text-gray-600 dark:text-gray-300">{parsedData.margin}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
