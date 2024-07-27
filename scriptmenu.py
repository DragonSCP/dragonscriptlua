-- scriptmenu.py
-- Menu Simples com interface gráfica usando Drawing

-- Função para criar uma interface com fundo de imagem
local menu = {
    visible = true,
    minimized = false,
    title = "Level Farm",
    options = {
        {name = "Level Farm", active = false}
    },
    uiElements = {},
    closeButtonArea = {x1 = 550, y1 = 310, x2 = 570, y2 = 330}, -- Área do botão de fechar
    backgroundImage = "https://i.ibb.co/8xTNLkj/940496-768-1024.webp" -- URL da imagem de fundo
}

-- Função para criar elementos de interface
function menu:createUI()
    -- Fundo do Menu com Imagem
    self.uiElements.background = Drawing.new("Image")
    self.uiElements.background.Visible = self.visible
    self.uiElements.background.Data = game:HttpGet(self.backgroundImage) -- Carrega a imagem
    self.uiElements.background.Size = Vector2.new(250, 250)
    self.uiElements.background.Position = Vector2.new(300, 300)
    
    -- Título
    self.uiElements.title = Drawing.new("Text")
    self.uiElements.title.Visible = self.visible
    self.uiElements.title.Text = self.title
    self.uiElements.title.Position = Vector2.new(310, 310)
    self.uiElements.title.Color = Color3.fromRGB(255, 255, 255)
    self.uiElements.title.Size = 20

    -- Botão de Fechar
    self.uiElements.closeButton = Drawing.new("Text")
    self.uiElements.closeButton.Visible = self.visible
    self.uiElements.closeButton.Text = "[X]"
    self.uiElements.closeButton.Position = Vector2.new(550, 310)
    self.uiElements.closeButton.Color = Color3.fromRGB(255, 0, 0)
    self.uiElements.closeButton.Size = 20

    -- Opções com caixas de seleção
    for i, option in ipairs(self.options) do
        local optionText = Drawing.new("Text")
        optionText.Visible = self.visible
        optionText.Text = (option.active and "[x] " or "[ ] ") .. option.name
        optionText.Position = Vector2.new(310, 330 + (i * 20))
        optionText.Color = Color3.fromRGB(255, 255, 255)
        optionText.Size = 18
        
        self.uiElements["option" .. i] = optionText
    end
end

-- Função para atualizar a interface do menu
function menu:updateUI()
    self.uiElements.background.Visible = self.visible
    self.uiElements.title.Visible = self.visible
    self.uiElements.closeButton.Visible = self.visible
    
    for i, option in ipairs(self.options) do
        local optionText = self.uiElements["option" .. i]
        optionText.Text = (option.active and "[x] " or "[ ] ") .. option.name
        optionText.Visible = self.visible
    end
end

-- Função para alternar visibilidade
function menu:toggleVisibility()
    self.visible = not self.visible
    self:updateUI()
end

-- Função para alternar minimização
function menu:toggleMinimize()
    if not self.visible then return end
    self.minimized = not self.minimized
    if self.minimized then
        self.uiElements.background.Size = Vector2.new(250, 30)
    else
        self.uiElements.background.Size = Vector2.new(250, 250)
    end
end

-- Função para verificar se o clique está dentro da área
function isClickInArea(x, y, area)
    return x >= area.x1 and x <= area.x2 and y >= area.y1 and y <= area.y2
end

-- Função para detectar cliques do jogador
function detectClicks()
    while true do
        local mouseX, mouseY = mouse.X, mouse.Y -- Ajuste para obter a posição do mouse
        local clicked = mouse.IsMouseButtonPressed(Enum.UserInputType.MouseButton1) -- Verifica se o botão do mouse foi pressionado

        if clicked then
            if isClickInArea(mouseX, mouseY, menu.closeButtonArea) then
                menu:toggleVisibility()
            else
                -- Verifica se o clique está na área de uma opção e alterna o estado
                for i, option in ipairs(menu.options) do
                    local optionText = menu.uiElements["option" .. i]
                    local optionArea = {
                        x1 = optionText.Position.X,
                        y1 = optionText.Position.Y,
                        x2 = optionText.Position.X + optionText.Size.X,
                        y2 = optionText.Position.Y + optionText.Size.Y
                    }
                    if isClickInArea(mouseX, mouseY, optionArea) then
                        option.active = not option.active
                        menu:updateUI()
                        if option.name == "Level Farm" then
                            -- Chama a função para iniciar o auto-farm
                            startAutoFarm()
                        end
                    end
                end
            end
        end
        
        wait(0.1) -- Pequena pausa para evitar uso excessivo de CPU
    end
end

-- Função para iniciar o auto-farm
function startAutoFarm()
    local autoFarmScriptUrl = "https://raw.githubusercontent.com/DragonSCP/dragonscriptlua/main/autofarm.py"
    local autoFarmScript = game:HttpGet(autoFarmScriptUrl)
    loadstring(autoFarmScript)()
end

-- Inicialização do Menu
menu:createUI()

-- Inicia a detecção de cliques
detectClicks()
