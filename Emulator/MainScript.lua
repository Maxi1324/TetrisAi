-- Script für verbindung mit Python Tetris AI
-- Author Maximilain Fischer 3BHIF
local socket = require("socket.core"); -- import the Socket package and make it accessable able via the Variable
local host, port = "127.0.0.1", 55535; -- stores the host and port for the connection with the PP(Python Program) str, int

local connected = false -- stores if connected to PP
local gameLoaded = false -- stores if game hase been initialized

local frame = 0 -- stores the active Frame; needed for the initialization of the Game    Int
local sec = false -- is set True every second Frame; needed for Input, because in oder to press a Button, the but have to be released befrore  bool 

local lastInfo = ""

-- Update: 
-- Update is called for each Frame, when the Input is polled
-- Update is managing what is done, an when

function update()
    if not gameLoaded then
        loadGame()
    else
        if connected then
            if (sec) then
                if (needToRes()) then
                    SendRevData()
                    sec = false
                end
            else
                sec = true
            end
        else
            connect()
        end
    end
end

-- loadGame
-- loadGame is called at the beginning of the Emulation to set up the Game

function loadGame()
    if sec then
        sec = false
        return
    end
    if frame < 109 + 2 then
        frame = frame + 1
        emu.setInput(0, {start = true})
    else
        emu.log("ready")
        emu.saveSavestateAsync(5)
        gameLoaded = true
    end
    sec = true
end

-- connect
-- connect is handling the connection to the PP
-- Before the Status and the Inputs can be resived, a connection have to be established.
-- thats what this function doe

function connect()
    local tcp = initSocket()
    tcp:send("start")
    local mes = tcp:receive(5);
    if (mes == "start") then connected = true end
end

-- SendRevData
-- When the Connection is there infos can be transmitted, thats what this function does.
-- This function is managing, the transfare of the infromation

function SendRevData()
    local tcp = initSocket();
    tcp:send(getInfo() .. ":" .. getNextBlock() .. ":" .. readScore())
    useInfo(tcp:receive(5), tcp)
end

-- getInfo:
-- calculate the information, that is send to the PP
-- Return: string which can be transmitted

function getInfo()
    local str = ""
    for j = 0, 19, 1 do
        for i = 0, 9, 1 do
            local x = i * 7.7 + 96 + 4
            local y = j * 7.95 + 48 + 4
            local wert = 1
            local f = emu.getPixel(x, y);
            if (not (emu.getPixel(x, y) > 0x000000)) then
                f = 0x60505050
                wert = 0
            end

            -- emu.drawRectangle(x, y,6, 5,f , true)
            str = str .. tostring(wert)
        end
    end
  
    return str
end

-- useInfo
-- useInfo does exactly, what the name suggest. It uses the Data and transforms it into inputs
-- Parameter:    Data
--              Socket

function useInfo(str, socket)
    inputs = {}
    for i = 1, 5 do inputs[i] = str:sub(i, i) == "1" end
    emu.setInput(0, {
        a = inputs[1],
        down = inputs[2],
        left = inputs[3],
        right = inputs[4]
    })
    if (inputs[5]) then
        -- socket:send(readScore())
        Reset()
    end
end

-- getNextBlock
-- reads the information from the RAM, which block comes next
-- Retrun: returns a string

function getNextBlock()
    local number = (emu.read(191, emu.memType.cpu, false))
    local numbers = {}
    numbers[0] = 2
    numbers[1] = 7
    numbers[2] = 8
    numbers[3] = 10
    numbers[4] = 11
    numbers[5] = 14
    numbers[6] = 18

    local teiler = 7

    local result = -1;

    for i = 0, 6, 1 do
        if (numbers[i] == number) then result = 1 / teiler * i end
    end
    return string.format("%.1f", result)
end

-- readScore
-- reads the Score, but in a wired way
-- it returns a string which can be interpreted in the PP
-- Return String

function readScore()
    local str1 = tostring(emu.read(117, emu.memType.cpu, false))
    local str2 = tostring(emu.read(116, emu.memType.cpu, false))
    local str3 = tostring(emu.read(115, emu.memType.cpu, false))

    return str3 .. ";" .. str2 .. ";" .. str1 .. ";"
end

-- Reset
-- The Reset function Resets the Game to the initinal state
-- It disconnect the conncection and load a GameSave to reset the Game itself

function Reset()
    emu.log("reset");
    connected = false;
    emu.loadSavestateAsync(5)
end

-- initSocket
-- creates a socket which trys to connect to the PP
-- the IP and the Port are taken from the attributes

function initSocket()
    local tcp = assert(socket.tcp());
    -- tcp:settimeout(1)
    tcp:connect(host, port);
    return tcp
end

function needToRes()
    local LInfo = getInfo();
    local bool = ( (lastInfo) == (LInfo))
    
    --emu.log(LInfo..":"..lastInfo.."="..tostring(bool))
    
    lastInfo = LInfo
    return bool
  end

-- adds the Update methode as a Callaback for the InputPolled Event
emu.addEventCallback(update, emu.eventType.inputPolled);

