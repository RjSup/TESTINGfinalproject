<script>
    let investmentAmount = '';
    let currentSavings = '';
    let riskTolerance = 5;
    let industryPreference = '';
    let loading = false;
    let error = null;
    let result = null;
    let questionIndex = 0;

    const questions = [
        { label: 'Investment Amount', bindVar: 'investmentAmount', placeholder: 'Enter amount', type: 'number' },
        { label: 'Current Savings', bindVar: 'currentSavings', placeholder: 'Enter savings', type: 'number' },
        { label: 'Risk Tolerance', bindVar: 'riskTolerance', type: 'range', min: 1, max: 10 },
        { label: 'Preferred Industry', bindVar: 'industryPreference', placeholder: 'e.g., Technology, Healthcare', type: 'text' }
    ];

    async function handleNext() {
        if (questionIndex < questions.length - 1) {
            questionIndex += 1;
        } else {
            await handleSubmit();
        }
    }

    async function handleSubmit() {
        loading = true;
        error = null;
        result = null;

        try {
            const payload = {
                investment_amount: Number(investmentAmount),
                current_savings: Number(currentSavings),
                risk_tolerance: Number(riskTolerance),
                industry: industryPreference
            };

            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            if (!data.success) throw new Error(data.error || 'Calculation failed');
            result = data;
        } catch (err) {
            error = err.message;
        } finally {
            loading = false;
        }
    }
</script>

<div class="min-h-screen w-full bg-white px-4 py-12">
    <div class="max-w-xl mx-auto">
        <h1 class="text-3xl font-bold text-gray-900 mb-8">WealthWise</h1>
        
        <!-- Progress indicator -->
        <div class="mb-8">
            <div class="h-1 bg-gray-100 rounded-full">
                <div class="h-1 bg-blue-500 rounded-full transition-all duration-300" 
                     style="width: {((questionIndex + 1) / questions.length) * 100}%">
                </div>
            </div>
            <p class="mt-2 text-sm text-gray-500 text-right">Step {questionIndex + 1} of {questions.length}</p>
        </div>

        {#if questionIndex < questions.length}
            <div class="space-y-6">
                <h2 class="text-xl font-medium text-gray-700">
                    {questions[questionIndex].label}
                </h2>

                {#if questions[questionIndex].type === 'number'}
                    {#if questions[questionIndex].bindVar === 'investmentAmount'}
                        <input 
                            type="number"
                            bind:value={investmentAmount}
                            class="w-full p-3 text-lg text-gray-700 border border-gray-200 rounded-lg focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
                            placeholder={questions[questionIndex].placeholder}
                        />
                    {:else}
                        <input 
                            type="number"
                            bind:value={currentSavings}
                            class="w-full p-3 text-lg text-gray-700 border border-gray-200 rounded-lg focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
                            placeholder={questions[questionIndex].placeholder}
                        />
                    {/if}
                {/if}

                {#if questions[questionIndex].type === 'range'}
                    <div>
                        <p class="text-lg mb-3">Risk Level: {riskTolerance}</p>
                        <input 
                            type="range"
                            bind:value={riskTolerance}
                            min={questions[questionIndex].min}
                            max={questions[questionIndex].max}
                            class="w-full h-2 bg-gray-100 rounded-full appearance-none cursor-pointer"
                        />
                        <div class="flex justify-between mt-2 text-sm text-gray-500">
                            <span>Conservative</span>
                            <span>Aggressive</span>
                        </div>
                    </div>
                {/if}

                {#if questions[questionIndex].type === 'text'}
                    <input 
                        type="text"
                        bind:value={industryPreference}
                        class="w-full p-3 text-lg text-gray-700 border border-gray-200 rounded-lg focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
                        placeholder={questions[questionIndex].placeholder}
                    />
                {/if}

                <button 
                    on:click={handleNext}
                    class="w-full p-4 text-lg font-medium text-white bg-blue-500 rounded-lg hover:bg-blue-600 focus:ring-4 focus:ring-blue-100 transition-colors"
                >
                    {questionIndex < questions.length - 1 ? 'Continue' : 'Calculate Risk'}
                </button>
            </div>
        {/if}

        {#if error}
            <div class="mt-6 p-4 text-red-600 bg-red-50 rounded-lg">
                <p>{error}</p>
            </div>
        {/if}

        {#if result}
            <div class="mt-8 space-y-6">
                <div class="border-t pt-6">
                    <h2 class="text-xl font-medium text-gray-900 mb-4">Your Risk Profile</h2>
                    <div class="space-y-3">
                        <div class="flex justify-between items-center">
                            <span class="text-gray-600">Risk Score</span>
                            <span class="font-medium">{result.risk_score}</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-gray-600">Risk Level</span>
                            <span class="font-medium">{result.risk_level}</span>
                        </div>
                    </div>
                </div>

                <div class="border-t pt-6">
                    <h2 class="text-xl font-medium text-gray-900 mb-4">Recommended Portfolio</h2>
                    <div class="space-y-3">
                        <div class="flex justify-between items-center">
                            <span class="text-gray-600">Stocks</span>
                            <span class="font-medium">{result.portfolio.stocks}%</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-gray-600">Bonds</span>
                            <span class="font-medium">{result.portfolio.bonds}%</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-gray-600">Cash</span>
                            <span class="font-medium">{result.portfolio.cash}%</span>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>