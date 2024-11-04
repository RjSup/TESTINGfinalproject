<script>
    export let portfolio;
    export let rebalanceDate;
</script>

<div class="border-t pt-6">
    <h2 class="text-xl font-medium text-gray-900 mb-4">Recommended Portfolio</h2>
    <div class="space-y-4">
        {#each portfolio as stock}
            <div class="p-4 border rounded-lg hover:shadow-md transition-shadow">
                <div class="space-y-2">
                    <div>
                        <h3 class="font-medium text-gray-900">{stock.company}</h3>
                        <p class="text-sm text-gray-500">{stock.industry}</p>
                    </div>
                    <div class="flex justify-between items-center text-sm">
                        <span class="text-gray-600">Allocation</span>
                        <span class="font-medium">£{stock.allocation.toLocaleString()}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm">
                        <span class="text-gray-600">Shares</span>
                        <span class="font-medium">{stock.shares}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm">
                        <span class="text-gray-600">Current Price</span>
                        <span class="font-medium">£{stock.current_price}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm">
                        <span class="text-gray-600">Predicted Price</span>
                        <span class="font-medium text-green-600">£{stock.predicted_price}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm">
                        <span class="text-gray-600">Predicted Return</span>
                        <span class="font-medium {stock.predicted_return >= 0 ? 'text-green-600' : 'text-red-600'}">
                            {stock.predicted_return}%
                        </span>
                    </div>
                    <div class="flex justify-between items-center text-sm">
                        <span class="text-gray-600">Predicted Gain</span>
                        <span class="font-medium {stock.predicted_gain >= 0 ? 'text-green-600' : 'text-red-600'}">
                            £{stock.predicted_gain.toLocaleString()}
                        </span>
                    </div>
                </div>
            </div>
        {/each}
    </div>
    <div class="text-sm text-gray-500 mt-4">
        Next Portfolio Rebalance: {rebalanceDate}
    </div>
</div>