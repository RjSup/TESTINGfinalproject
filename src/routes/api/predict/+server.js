import { json } from '@sveltejs/kit';
import { spawn } from 'child_process';
import path from 'path';

export async function POST({ request }) {
    try {
        const data = await request.json();
        console.log('API endpoint hit with data:', JSON.stringify(data, null, 2));

        // Validate input data
        if (!data.investment_amount || !data.risk_tolerance) {
            console.log('Validation failed: Missing required fields');
            return json({
                success: false,
                error: "Missing required fields"
            }, { status: 400 });
        }

        const scriptPath = path.join(process.cwd(), 'src', 'lib', 'ML', 'main.py');
        console.log('Executing Python script at:', scriptPath);

        return new Promise((resolve) => {
            const pythonProcess = spawn('python.exe', [scriptPath]);
            let outputData = '';
            let errorData = '';

            pythonProcess.stdin.write(JSON.stringify(data));
            pythonProcess.stdin.end();

            pythonProcess.stdout.on('data', (data) => {
                outputData += data.toString();
            });

            pythonProcess.stderr.on('data', (data) => {
                errorData += data.toString();
                console.error('Python stderr:', data.toString());
            });

            pythonProcess.on('close', (code) => {
                console.log('Python process closed with code:', code);
                console.log('Raw output:', outputData);

                if (code !== 0) {
                    console.error('Python script error:', errorData);
                    return resolve(json({
                        success: false,
                        error: "Error executing Python script"
                    }, { status: 500 }));
                }

                try {
                    const jsonStartIndex = outputData.indexOf('{');
                    const jsonString = outputData.substring(jsonStartIndex);
                    const result = JSON.parse(jsonString);
                    resolve(json(result));
                } catch (e) {
                    console.error('JSON parse error:', e);
                    console.error('Raw output:', outputData);
                    resolve(json({
                        success: false,
                        error: "Error parsing prediction results"
                    }, { status: 500 }));
                }
            });
        });
    } catch (error) {
        console.error('API error:', error);
        return json({
            success: false,
            error: "Internal server error"
        }, { status: 500 });
    }
}