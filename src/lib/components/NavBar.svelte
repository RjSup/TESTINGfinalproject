<script>
    import { slide } from 'svelte/transition';
  
    let isOpen = false;
    
  
    function toggleMenu() {
      isOpen = !isOpen;
    }
  </script>
  
  <nav class="bg-white">
    <div class="max-w-6xl mx-auto px-4">
      <div class="flex justify-between items-center">
        <div class="flex-shrink-0">
          <a href="/" class="flex items-center py-4 px-2">
            <span class="font-semibold text-gray-500 text-lg hover:text-green-500">WealthWise</span>
          </a>
        </div>
        <div class="hidden md:flex items-center space-x-1">
          <a href="/" class="py-4 px-2 text-gray-500 font-semibold hover:text-green-500 transition duration-300">Home</a>
          <a href="/about" class="py-4 px-2 text-gray-500 font-semibold hover:text-green-500 transition duration-300">About</a>
        </div>
        <div class="md:hidden flex items-center">
          <button on:click={toggleMenu} class="outline-none mobile-menu-button" aria-label="Toggle menu">
            {#if isOpen}
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            {:else}
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            {/if}
          </button>
        </div>
      </div>
    </div>
    {#if isOpen}
      <div transition:slide class="md:hidden">
        <a href="/" class="block py-2 px-4 text-sm hover:bg-gray-200">Home</a>
        <a href="/about" class="block py-2 px-4 text-sm hover:bg-gray-200">About</a>
      </div>
    {/if}
  </nav>