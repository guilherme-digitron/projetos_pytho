document.addEventListener('DOMContentLoaded', () => {
    // Referências aos Elementos da UI
    const card = document.getElementById('game-card');
    const cardCharacter = document.getElementById('card-character');
    const cardText = document.getElementById('card-text');
    const choiceLeftText = document.getElementById('choice-left');
    const choiceRightText = document.getElementById('choice-right');
    const dayCounter = document.getElementById('day-counter');

    const mentalBar = document.getElementById('mental-bar');
    const socialBar = document.getElementById('social-bar');
    const energyBar = document.getElementById('energy-bar');
    const onlineBar = document.getElementById('online-bar');

    const gameOverScreen = document.getElementById('game-over-screen');
    const gameOverTitle = document.getElementById('game-over-title');
    const gameOverMessage = document.getElementById('game-over-message');
    const restartButton = document.getElementById('restart-button');

    // Estado do Jogo
    let gameState = {};

    // Dados das Cartas
    const cards = [
        {
            character: "Sua Mente",
            text: "Seu feed está cheio de pessoas em férias incríveis. Parece que todos estão mais felizes que você.",
            choiceLeft: "Fechar o app e meditar.",
            choiceRight: "Continuar rolando a tela.",
            effectLeft: { mental: 15, social: 0, energy: 5, online: -10 },
            effectRight: { mental: -15, social: 0, energy: -5, online: 5 },
        },
        {
            character: "Amigo",
            text: "Vamos sair hoje à noite! Vai ter uma festa legal.",
            choiceLeft: "Não, prefiro ficar em casa.",
            choiceRight: "Claro, vamos!",
            effectLeft: { mental: 5, social: -15, energy: 5, online: 10 },
            effectRight: { mental: 10, social: 20, energy: -15, online: -10 },
        },
        {
            character: "Notificação",
            text: "Seu celular apita. É 1h da manhã. Uma nova trend surgiu no TikTok.",
            choiceLeft: "Ignorar e ir dormir.",
            choiceRight: "Só uma olhadinha...",
            effectLeft: { mental: 10, social: 0, energy: 15, online: -5 },
            effectRight: { mental: -10, social: 0, energy: -20, online: 15 },
        },
        {
            character: "Trabalho da Escola",
            text: "Você tem um projeto importante para entregar amanhã.",
            choiceLeft: "Procrastinar no YouTube.",
            choiceRight: "Focar e terminar logo.",
            effectLeft: { mental: -15, social: 0, energy: -20, online: 10 },
            effectRight: { mental: 10, social: 0, energy: 15, online: -10 },
        },
        {
            character: "Grupo da Família",
            text: "Uma nova teoria da conspiração está bombando no grupo.",
            choiceLeft: "Silenciar o grupo.",
            choiceRight: "Entrar na discussão.",
            effectLeft: { mental: 10, social: -5, energy: 0, online: -5 },
            effectRight: { mental: -20, social: 5, energy: -10, online: 10 },
        },
        {
            character: "Sol",
            text: "O dia está lindo lá fora. Uma caminhada no parque seria ótima.",
            choiceLeft: "Boa ideia, vou agora!",
            choiceRight: "Nah, maratonar série.",
            effectLeft: { mental: 20, social: 5, energy: 10, online: -15 },
            effectRight: { mental: -10, social: -10, energy: -5, online: 15 },
        },
        {
            character: "Desconhecido",
            text: "Você recebe um comentário maldoso em uma foto sua.",
            choiceLeft: "Ignorar e bloquear.",
            choiceRight: "Responder no mesmo nível.",
            effectLeft: { mental: 5, social: 0, energy: 0, online: -5 },
            effectRight: { mental: -25, social: 0, energy: -10, online: 10 },
        }
    ];

    // Lógica de Interação com a Carta
    let isDragging = false;
    let startX = 0;
    let currentX = 0;

    function startDrag(e) {
        isDragging = true;
        startX = e.pageX || e.touches[0].pageX;
        card.classList.add('dragging');
    }

    function onDrag(e) {
        if (!isDragging) return;
        currentX = (e.pageX || e.touches[0].pageX) - startX;
        const rotation = currentX / 20;
        
        card.style.transform = `translateX(${currentX}px) rotate(${rotation}deg)`;

        const opacity = Math.abs(currentX) / 100;
        if (currentX > 0) {
            choiceRightText.style.opacity = opacity;
            choiceLeftText.style.opacity = 0;
        } else {
            choiceLeftText.style.opacity = opacity;
            choiceRightText.style.opacity = 0;
        }
    }

    function endDrag() {
        if (!isDragging) return;
        isDragging = false;
        card.classList.remove('dragging');

        const threshold = 100;
        if (currentX > threshold) {
            handleChoice('right');
        } else if (currentX < -threshold) {
            handleChoice('left');
        } else {
            resetCardPosition();
        }
    }
    
    function handleChoice(direction) {
        card.style.transition = 'transform 0.4s ease';
        const flyOutX = direction === 'right' ? window.innerWidth : -window.innerWidth;
        card.style.transform = `translateX(${flyOutX}px) rotate(${direction === 'right' ? 30 : -30}deg)`;

        const cardData = cards[gameState.currentCardIndex];
        const effect = direction === 'right' ? cardData.effectRight : cardData.effectLeft;

        setTimeout(() => {
            updateStats(effect);
            gameState.day++;
            gameState.currentCardIndex = (gameState.currentCardIndex + 1) % cards.length;
            
            if (!checkForGameOver()) {
                loadNextCard();
            }
        }, 400);
    }
    
    function resetCardPosition() {
        card.style.transform = 'translateX(0) rotate(0deg)';
        choiceLeftText.style.opacity = 0;
        choiceRightText.style.opacity = 0;
    }

    // Lógica do Jogo
    function startGame() {
        gameState = {
            stats: { mental: 50, social: 50, energy: 50, online: 50 },
            day: 1,
            currentCardIndex: 0
        };
        shuffleArray(cards);
        gameOverScreen.classList.remove('visible');
        loadNextCard();
        updateUI();
    }

    function loadNextCard() {
        const cardData = cards[gameState.currentCardIndex];
        card.style.opacity = 0;
        setTimeout(() => {
            resetCardPosition();
            cardCharacter.textContent = cardData.character;
            cardText.textContent = cardData.text;
            choiceLeftText.textContent = cardData.choiceLeft;
            choiceRightText.textContent = cardData.choiceRight;
            card.style.opacity = 1;
            updateUI();
        }, 200);
    }

    function updateStats(effect) {
        for (const stat in effect) {
            gameState.stats[stat] += effect[stat];
            gameState.stats[stat] = Math.max(0, Math.min(100, gameState.stats[stat]));
        }
    }

    function updateUI() {
        mentalBar.style.width = `${gameState.stats.mental}%`;
        socialBar.style.width = `${gameState.stats.social}%`;
        energyBar.style.width = `${gameState.stats.energy}%`;
        onlineBar.style.width = `${gameState.stats.online}%`;
        dayCounter.textContent = `Dia ${gameState.day}`;
    }
    
    function checkForGameOver() {
        const stats = gameState.stats;
        let gameOver = false;
        let message = "";
        let title = "Fim de Jogo";

        if (stats.mental <= 0) {
            gameOver = true;
            message = "Você se sentiu sobrecarregado e exausto. O esgotamento mental tomou conta.";
        } else if (stats.mental >= 100) {
            gameOver = true;
            title = "Paz Interior";
            message = "Você alcançou um estado de clareza e paz mental. Um equilíbrio perfeito!";
        } else if (stats.social <= 0) {
            gameOver = true;
            message = "O isolamento se tornou sua realidade. Você se afastou de todos.";
        } else if (stats.social >= 100) {
            gameOver = true;
            message = "Você se doou tanto aos outros que esqueceu de cuidar de si mesmo.";
        } else if (stats.energy <= 0) {
            gameOver = true;
            message = "Sem energia para nada, seus dias se tornaram um borrão de cansaço.";
        } else if (stats.energy >= 100) {
            gameOver = true;
            title = "Pura Produtividade";
            message = "Com energia de sobra, você conquistou todos os seus objetivos!";
        } else if (stats.online <= 0) {
            gameOver = true;
            message = "Totalmente desconectado, você se sentiu perdido e de fora do mundo.";
        } else if (stats.online >= 100) {
            gameOver = true;
            message = "A vida digital consumiu você. A realidade ficou em segundo plano.";
        }

        if (gameOver) {
            showGameOverScreen(title, message);
        }
        return gameOver;
    }

    function showGameOverScreen(title, message) {
        gameOverTitle.textContent = title;
        gameOverMessage.textContent = message;
        gameOverScreen.classList.add('visible');
    }
    
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    // Event Listeners
    card.addEventListener('mousedown', startDrag);
    document.addEventListener('mousemove', onDrag);
    document.addEventListener('mouseup', endDrag);
    
    card.addEventListener('touchstart', startDrag, { passive: true });
    document.addEventListener('touchmove', onDrag, { passive: true });
    document.addEventListener('touchend', endDrag);
    
    restartButton.addEventListener('click', startGame);

    // Iniciar o jogo
    startGame();
});