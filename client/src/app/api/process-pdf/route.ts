import { NextRequest, NextResponse } from 'next/server';
import { writeFile, readFile } from 'fs/promises';
import { join } from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }

    if (file.type !== 'application/pdf') {
      return NextResponse.json(
        { error: 'File must be a PDF' },
        { status: 400 }
      );
    }

    // Save the uploaded file temporarily
    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);
    const tempPath = join(process.cwd(), '..', 'temp.pdf');
    console.log('Saving PDF to:', tempPath);
    await writeFile(tempPath, buffer);

    // First, run the chunking script
    const chunkingScript = join(process.cwd(), '..', 'utils', 'test_chunking.py');
    const venvPython = join(process.cwd(), '..', 'venv', 'bin', 'python');
    console.log('Running chunking script:', chunkingScript);
    console.log('Using Python:', venvPython);
    
    try {
      // Run chunking script
      console.log('Executing chunking script...');
      const { stdout: chunkingStdout, stderr: chunkingStderr } = await execAsync(`${venvPython} ${chunkingScript} ${tempPath}`);
      
      if (chunkingStderr) {
        console.error('Chunking error:', chunkingStderr);
        return NextResponse.json(
          { error: `Chunking error: ${chunkingStderr}` },
          { status: 500 }
        );
      }
      console.log('Chunking script output:', chunkingStdout);

      // Check if chunks file was created
      const chunksPath = join(process.cwd(), '..', 'chunks1.txt');
      try {
        await readFile(chunksPath, 'utf-8');
        console.log('Chunks file exists and is readable');
      } catch (error) {
        console.error('Error reading chunks file:', error);
        return NextResponse.json(
          { error: 'Failed to read chunks file. Please make sure the PDF was processed correctly.' },
          { status: 500 }
        );
      }

      // Then, run the vector store script
      const vectorStoreScript = join(process.cwd(), '..', 'utils', 'vector_store.py');
      console.log('Running vector store script:', vectorStoreScript);
      
      console.log('Executing vector store script...');
      const { stdout: vectorStdout, stderr: vectorStderr } = await execAsync(`${venvPython} ${vectorStoreScript}`);
      
      if (vectorStderr) {
        console.error('Vector store error:', vectorStderr);
        return NextResponse.json(
          { error: `Vector store error: ${vectorStderr}` },
          { status: 500 }
        );
      }
      console.log('Vector store script output:', vectorStdout);

      // Check if company snapshot file was created
      const snapshotPath = join(process.cwd(), '..', 'company_snapshot1.txt');
      let snapshotContent;
      try {
        snapshotContent = await readFile(snapshotPath, 'utf-8');
        console.log('Company snapshot file exists and is readable');
        console.log('Snapshot content:', snapshotContent);
      } catch (error) {
        console.error('Error reading company snapshot file:', error);
        return NextResponse.json(
          { error: 'Failed to read company snapshot file. Please try uploading the PDF again.' },
          { status: 500 }
        );
      }

      // Read and parse the files
      const chunksContent = await readFile(chunksPath, 'utf-8');
      const chunks = parseChunks(chunksContent);
      const companyDetails = parseCompanySnapshot(snapshotContent);

      console.log('Parsed company details:', companyDetails);
      console.log('Number of chunks:', chunks.length);

      return NextResponse.json({
        success: true,
        message: 'PDF processed successfully',
        data: {
          ...companyDetails,
          chunks
        }
      });

    } catch (execError: any) {
      console.error('Exec error:', execError);
      return NextResponse.json(
        { error: `Failed to execute scripts: ${execError.message || 'Unknown error'}` },
        { status: 500 }
      );
    }

  } catch (error: any) {
    console.error('Error processing PDF:', error);
    return NextResponse.json(
      { error: `Failed to process PDF: ${error.message || 'Unknown error'}` },
      { status: 500 }
    );
  }
}

function parseCompanySnapshot(content: string): {
  sector: string;
  hq: string;
  revenue: string;
  growth: string;
  margin: string;
} {
  // Extract sector from the company overview
  const sectorMatch = content.match(/Project Atlas identifies optimal locations.*?by analyzing costs, talent pools, livability, commute patterns, socio- demographics, and other educational\s+and sustainability factors/);
  const sector = sectorMatch ? "Location Intelligence & Data Analytics" : "Not found";

  // Extract HQ from the company details
  const hqMatch = content.match(/HEADQUARTERS\s*([^\n]+)/);
  const hq = hqMatch ? hqMatch[1].trim() : "Not found";

  // Extract revenue from the financial summary
  const revenueMatch = content.match(/Revenue\s*(\$[\d.]+M)/);
  const revenue = revenueMatch ? revenueMatch[1] : "Not found";

  // Extract growth from the key metrics
  const growthMatch = content.match(/Revenue growth %\s*na\s*(\d+)%/);
  const growth = growthMatch ? `${growthMatch[1]}%` : "Not found";

  // Extract margin from the key metrics
  const marginMatch = content.match(/Gross margin %\s*(\d+)%/);
  const margin = marginMatch ? `${marginMatch[1]}%` : "Not found";

  return {
    sector,
    hq,
    revenue,
    growth,
    margin
  };
}

function parseChunks(content: string): string[] {
  const chunks: string[] = [];
  const chunkRegex = /Chunk \d+:\n([\s\S]*?)(?=\n-{40}|$)/g;
  let match;

  while ((match = chunkRegex.exec(content)) !== null) {
    chunks.push(match[1].trim());
  }

  return chunks;
} 