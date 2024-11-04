<script>
    export let question;
    export let investmentAmount;
    export let currentSavings;
    export let riskTolerance;
    export let industryPreference;
    export let onNext;
    export let isLastQuestion;
</script>

<div class="space-y-6">
    <h2 class="text-xl font-medium text-gray-700">
        {question.label}
    </h2>

    {#if question.type === 'number'}
        {#if question.bindVar === 'investmentAmount'}
            <input 
                type="number"
                bind:value={investmentAmount}
                class="w-full p-3 text-lg text-gray-700 border border-gray-200 rounded-lg focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-colors"
                placeholder={question.placeholder}
            />
        {:else}
            <input 
                type="number"
                bind:value={currentSavings}
                class="w-full p-3 text-lg text-gray-700 border border-gray-200 rounded-lg focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-colors"
                placeholder={question.placeholder}
            />
        {/if}
    {/if}

    {#if question.type === 'range'}
        <div>
            <p class="text-lg mb-3">Risk Level: {riskTolerance}</p>
            <input 
                type="range"
                bind:value={riskTolerance}
                min={question.min}
                max={question.max}
                class="w-full h-2 bg-gray-100 rounded-full appearance-none cursor-pointer"
            />
            <div class="flex justify-between mt-2 text-sm text-gray-500">
                <span>Conservative</span>
                <span>Aggressive</span>
            </div>
        </div>
    {/if}

    {#if question.type === 'text'}
        <input 
            type="text"
            bind:value={industryPreference}
            class="w-full p-3 text-lg text-gray-700 border border-gray-200 rounded-lg focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-colors"
            placeholder={question.placeholder}
        />
    {/if}

    <button 
        on:click={onNext}
        class="w-full p-4 text-lg font-medium text-white bg-green-500 rounded-lg hover:bg-green-600 focus:ring-4 focus:ring-green-100 transition-colors"
    >
        {isLastQuestion ? 'Calculate Risk' : 'Continue'}
    </button>
</div>