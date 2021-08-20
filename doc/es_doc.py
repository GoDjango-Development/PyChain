base_doc = \
        """Transfer File Blockchain es un modulo para gestion de operaciones sobre las criptomonedas a traves del protocolo TF (Trans
fer File), las operaciones que se pueden realizar con el son:
1- Transferencias: Permite las transferencias de criptomonedas de una direccion a otra... Para su uso es necesario una
llave privada (private key) o una contraseña en caso de Bitcoin (passphrase), de esta forma aseguramos la transferencia,
Ejemplos son:

bitcoin transfer to tb1qx8v84ysaw7fz8f0ps305cvrzrs2xrlt832sdc8 amount 0.001 fee 0.00001 with MyCustomPassphrase123!!!
ethereum transfer to 0x3cDb2F1d7F800CC2d72213B17AFc999a31D0e90e amount 0.001 with 78ebaebce1fb9f3ca35112557ec202abf43cea029c752f25230a43a266c1877f gas-price 2000 gas-limit 21000 
dai transfer to 0x3cDb2F1d7F800CC2d72213B17AFc999a31D0e90e amount 1 with 78ebaebce1fb9f3ca35112557ec202abf43cea029c75 fee 0.0001

Por una cuestion de facilidad de uso, los comandos o acciones tienen argumentos similares, asi siguiendo la siguiente sinta
xis logramos obtener una orden valida:

entorno + accion + argN + valN ... 

Entonces para todos los entornos tenemos acciones similares, siendo transfer comun para todos los entornos soportados
la accion transfer posee argumentos similares para todas las acciones por ejemplo, with de transfer es valida para todos
los entornos, aunque en el entorno bitcoin accion transfer with espera la passphrase para desbloquear la wallet y realizar
la transferencia, tener en cuenta que si usted pierde tanto la passphrase como la llave privada, usted perdera el acceso
a su cuenta y a su wallet, perdiendo todos sus fondos a menos que recuerde sus datos. Para mas informacion sobre como
funcionan las cuentas y wallets porfavor leerse la documentacion en https://ethereum.org/ y https://bitcoin.org/ 
2- Obtencion de datos: Permite obtener datos de una cuenta o de una transferencia, estos datos son los datos publicos 
de la blockchain, en caso de querer obtener datos privados como las llaves privadas, debemos acceder a la cuenta con
la llave privada. A continuacion ejemplos de obtencion de datos de la blockchain:

bitcoin get-balance
bitcoin get-raw-prik of tb1qx8v84ysaw7fz8f0ps305cvrzrs2xrlt832sdc8
bitcoin get-prik of tb1qx8v84ysaw7fz8f0ps305cvrzrs2xrlt832sdc8
bitcoin get-address
bitcoin get-pubk of tb1qx8v84ysaw7fz8f0ps305cvrzrs2xrlt832sdc8
bitcoin get-tx-status of <transaction_hash_goes_in_here_not_example_provided>
bitcoin get-fee
dai get-balance
dai get-raw-prik
dai get-prik
dai get-address
dai get-tx-status of <transaction_hash_goes_in_here_not_example_provided>
dai get-fee
ethereum get-balance
ethereum get-raw-prik
ethereum get-prik
ethereum get-address
ethereum get-tx-status of <transaction_hash_goes_in_here_not_example_provided>
ethereum get-fee

Los ejemplos anteriores pueden tener variaciones, estos ejemplos tienen como objetivo demostrar un resumen de las
opciones otorgadas por el modulo, para entrar en mas detalles sobre las acciones ver la seccion de acciones.
3- Establecimiento de datos: Esta seccion tiene como objetivos establecer contraseñas (Bitcoin), cuentas (para
trabajo posterior), proovedores o direcciones de nodos (tales como infura o otros), entre otras cosas... Debido a esto
una vez establecido los datos, no necesitamos volver a pasarlos para trabajar con nuestras cuentas y nodos. A conti
nuacion ejemplos:

bitcoin set-provider url http://username:password@ip:port
bitcoin set-account name AccountName
bitcoin set-wallet-passphrase with Passphrase123!!!
bitcoin set-fee amount 0.001
dai set-provider url https://mainnet.infura.io/v3/<your_api_key>
dai set-account prik <your-account-prik>
ethereum set-provider url https://mainnet.infura.io/v3/<your_api_key>
ethereum set-account prik <your-account-prik>

4- Miscelaneas: Otras funciones que tiene el modulo.... 

bitcoin lock-wallet // This command forces the wallet to be locked so anyone can do any kind of action
// over it without a passphrase. More info on action section on this documentation.

bitcoin unlock-wallet with Passphrase123!!! // This command unlock the wallet so anyone with access to the node
// can interact with your wallet... USE UNDER YOUR RISK.... DEFAULT TIMEOUT IS 3 SECONDS.... 

bitcoin change-passphrase old OldPassphrase123!!! new NewPassphrase123!!! // Modify current bitcoin wallet passphrase

5- Historicas: Permite el trabajo con una cache en el servidor TF, todas las acciones que realiza el usuario con
el modulo son almacenadas en cache excepto las acciones que revelen informacion privada como la llave privada.

bitcoin historic use 1
bitcoin historic get-all
bitcoin historic get-last
ethereum historic use 1
ethereum historic get-all
ethereum historic get-last
dai historic use 1
dai historic get-all
dai historic get-last

Los caches tienen un timestamp de la ultima vez que fueron modificados, cada vez que un usuario inicia el protocolo se
limpia la cache con 3 meses de antiguedad para ahorrar espacio..."""
dai_doc = \
    """Entorno Dai:
Acciones:
    transfer: Transfiere una cantidad X de Dai hacia una direccion X
Argumentos:
    to: Direccion de destino la cual recibira los dai que le envies. Valor esperado String.
    amount: Cantidad de dai a ser enviado. Valor esperado Float.
    gas-price: Impuesto a ser pagado a los mineros x cada byte consumido en la operacion. Valor esperado Float. 
    gas-limit: Maximo dispuesto a pagar por la transaccion.
    from: Direccion origen de la transaccion.
    with: Llave privada para firmar la transaccion.
Errores: 
    Codigo de error: 40
Retorna:
    Dict: Key + String(hash o transaction id)
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-balance: Obtiene el balance de una cuenta
Argumentos:
    of: direccion de la cual se quiere obtener el balance (Opcional)
Errores:
    Codigo de error: 50
Retorna:
    Dict: Key + float(balance)	
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    create-account: Crea una cuenta o wallet 
Argumentos:
    with: Llave privada de la direccion ethereum en caso de que quiera usar alguna direccion ethereum ya existente.
    (Opcional)
Errores:
    Codigo de error: 70
Retorna:
    Dict: Key + String(Address), Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-raw-prik: Obtiene la llave privada de la cuenta actual como una cadena formateada...
Argumentos:
    -
Errores:
    Codigo de error: 52
Retorna:
    Dict: Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-prik: Obtiene la llave privada de la cuenta actual en hexadecimal string.
Argumentos:
    -
Errores:
    Codigo de error: 51
Retorna:
    Dict: Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-address: Obtiene la direccion de la cuenta actual.
Argumentos:
    -
Errores:
    Codigo de error: 53
Retorna:
    Dict: Key + Dict(UTxOs)
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-tx-status: Obtiene el estado actual de una transaccion.
Argumentos:
    of: Transaction Id o Hash de la transaccion. Valor esperado, String
Errores:
    Codigo de error: 56
Retorna:
    Dict: Key + Dict(Transaction Details)

--------------------------------------------------------------------------------------------------------------------------
Acciones:
    create-wallet: Crea una cuenta. 
Argumentos:
    with: Llave privada de la direccion ethereum en caso de que quiera usar alguna direccion ethereum ya existente.
    (Opcional
Errores:
    Codigo de error: 70
Retorna:
    Dict: Key + String(Address), Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    set-provider: Establece un proveedor para las operaciones posteriores con la blockchain, esto puede ser un nodo,
    o una plataforma como Infura.
Argumentos:
    url: direccion http del nodo (Dai ERC20 es un token de ethereum por lo cual el nodo usado debe ser de ethereum).
Errores:
    Codigo de error: 62
Retorna:
    Dict: Key + Boolean
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    set-account: Establece una cuenta o wallet para trabajo posterior sobre ella.
Argumentos:
    with: Llave privada de la cuenta.
Errores:
    Codigo de error: 60
Retorna:
    Dict: Key + String(Name)
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-fee: Obtiene el fee estimado para una transaccion.
Argumentos:
    use: Cantidad de gas usado en la transaccion.
Errores:
    Codigo de error: 54
Retorna:
    Dict: Key + Float"""
btc_doc = \
    """Entorno Bitcoin:
Acciones:
    transfer: Transfiere una cantidad X de bitcoin hacia una direccion X
Argumentos:
    to: Direccion de destino la cual recibira los bitcoins que le envies. Valor esperado String.
    amount: Cantidad de bitcoin a ser enviado. Valor esperado Float.
    fee: Impuesto a ser pagado a los mineros. Este impuesto sera usado para las proximas transacciones en esta wallet
    a menos que establezca otro fee con el comando set-fee. Opcional: Smart Fee usado por defecto. Valor esperado
    Float. 
    replace: Establece si la transaccion podra ser reemplazada por otra transaccion con mayor fee o no. Valor esperado
    Booleano True or true, cualquier otro valor pasado sera considerado como false or False.
    passphrase: Desbloquea la wallet para permitir la transferencia, este parametro es requerido. Valor esperado 
    String
Errores: 
    Codigo de error: 40
Retorna:
    Dict: Key + String(hash o transaction id)
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-balance: Obtiene el balance de una wallet
Argumentos:
    base: BaseCurrency o moneda base, admite dos valores sat or btc, devuelve el balance en satoshi o en bitcoin.
    Por defecto devuelve en satoshi. Valor esperado: String "sat" or "btc"
Errores:
    Codigo de error: 50
Retorna:
    Dict: Key + float(balance)	
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    create-account: Crea una cuenta o wallet, y devuelve 
Argumentos:
    name: Nombre de la wallet de bitcoin.
Errores:
    Codigo de error: 70
Retorna:
    Dict: Key + String(Wallet Name)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-raw-prik: Obtiene la llave privada como una cade formateada...
Argumentos:
    of: La direccion de la cual se quiere obtener la llave privada.
Errores:
    Codigo de error: 52
Retorna:
    Dict: Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-prik: Obtiene la llave privada en hexadecimal string.
Argumentos:
    of: La direccion de la cual se quiere obtener la llave privada.
Errores:
    Codigo de error: 51
Retorna:
    Dict: Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-address: Obtiene todas las direcciones con UTxO (Unspent Trasnaction Output) o bitcoins en ellas.
Argumentos:
    -
Errores:
    Codigo de error: 53
Retorna:
    Dict: Key + Dict(UTxOs)
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-pubk: Obtiene la llave publica de una direccion.
Argumentos:
    of: Direccion de la cual se quiere obtener la llave publica.
Errores:
    Codigo de error: 55
Retorna:
    Dict: Key + String(Llave publica)
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-tx-status: Obtiene el estado actual de una transaccion.
Argumentos:
    of: Transaction Id o Hash de la transaccion. Valor esperado, String
Errores:
    Codigo de error: 56
Retorna:
    Dict: Key + Dict(Transaction Details)

--------------------------------------------------------------------------------------------------------------------------
Acciones:
    create-wallet: Crea una cuenta o wallet, y devuelve 
Argumentos:
    name: Nombre de la wallet de bitcoin.
Errores:
    Codigo de error: 70
Retorna:
    Dict: Key + String(Wallet Name)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    set-provider: Establece un proveedor para las operaciones posteriores con la blockchain, esto puede ser un nodo,
    o una plataforma que escuche JsonRPC de Bitcoin Core.
Argumentos:
    url: direccion http del nodo.
    user: Nombre de usuario necesario para los comandos rpc.
    pass: Contraseña necesaria para los comandos rpc.
    address: Direccion IP o DNS del nodo.
    port: Puerto TCP por el cual el nodo acepta los comandos rpc.
    protocol: Protocolo para la comunicacion con el nodo http o https.
Errores:
    Codigo de error: 62
Retorna:
    Dict: Key + Boolean
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    set-account: Establece una cuenta o wallet para trabajo posterior sobre ella.
Argumentos:
    with: Nombre de la wallet a ser establecida.
Errores:
    Codigo de error: 60
Retorna:
    Dict: Key + String(Name)
---------------------------------------------------------------------------------------------------------------------------
Acciones: 
    set-passphrase: Protege tu wallet mediante una contraseña.
Argumentos:
    with: Contraseña de la wallet.
Errores:
    Codigo de error: 63
Retorna:
    Dict: Key + Boolean
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    unlock-wallet: Desbloquea tu wallet para poder realizar operaciones sobre ella.
Argumentos:
    with: Contraseña de la wallet.
    timeout: Tiempo para que la wallet se vuelva a bloquear automaticamente (Opcional), Default = 3
Errores:
    Codigo de error: 81
Retorna:
    Dict: Key + Boolean
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    lock-wallet: Bloquea tu wallet para que nadie pueda realizar ninguna operacion sobre ella.
Argumentos:
    -
Errores:
    Codigo de error: 82
Retorna: 
    Dict: Key + Boolean
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    change-passphrase: Cambia la contraseña de tu wallet.
Argumentos:
    old: Antigua contraseña
    new: Nueva contraseña
Errores:
    Codigo de error: 80
Retorna:
    Dict: Key + Boolean
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-fee: Obtiene el fee estimado para una transaccion.
Argumentos:
    conf-target: 
    mode: 
Errores:
    Codigo de error: 54
Retorna:
    Dict: Key + Float
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    set-fee: Establece el fee a ser utilizado en una transaccion.
Argumentos:
    amount: Cantidad de fee.
Errores:
    Codigo de error: 61
Retorna:
    Dict: Key + Boolean"""
eth_doc = \
    """Entorno Ethereum:
Acciones:
    transfer: Transfiere una cantidad X de ethereum hacia una direccion X
Argumentos:
    to: Direccion de destino la cual recibira los ether que le envies. Valor esperado String.
    amount: Cantidad de ether a ser enviado. Valor esperado Float.
    gas-price: Impuesto a ser pagado a los mineros x cada byte consumido en la operacion. Valor esperado Float. 
    gas-limit: Maximo dispuesto a pagar por la transaccion.
    from: Direccion origen de la transaccion.
    with: Llave privada para firmar la transaccion.
Errores: 
    Codigo de error: 40
Retorna:
    Dict: Key + String(hash o transaction id)
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-balance: Obtiene el balance de una cuenta
Argumentos:
    of: direccion de la cual se quiere obtener el balance (Opcional)
Errores:
    Codigo de error: 50
Retorna:
    Dict: Key + float(balance)	
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    create-account: Crea una cuenta o wallet 
Argumentos:
    -
Errores:
    Codigo de error: 70
Retorna:
    Dict: Key + String(Address), Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-raw-prik: Obtiene la llave privada de la cuenta actual como una cadena formateada...
Argumentos:
    -
Errores:
    Codigo de error: 52
Retorna:
    Dict: Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-prik: Obtiene la llave privada de la cuenta actual en hexadecimal string.
Argumentos:
    -
Errores:
    Codigo de error: 51
Retorna:
    Dict: Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-address: Obtiene la direccion de la cuenta actual.
Argumentos:
    -
Errores:
    Codigo de error: 53
Retorna:
    Dict: Key + Dict(UTxOs)
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-tx-status: Obtiene el estado actual de una transaccion.
Argumentos:
    of: Transaction Id o Hash de la transaccion. Valor esperado, String
Errores:
    Codigo de error: 56
Retorna:
    Dict: Key + Dict(Transaction Details)

--------------------------------------------------------------------------------------------------------------------------
Acciones:
    create-wallet: Crea una cuenta. 
Argumentos:
    -
Errores:
    Codigo de error: 70
Retorna:
    Dict: Key + String(Address), Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    set-provider: Establece un proveedor para las operaciones posteriores con la blockchain, esto puede ser un nodo,
    o una plataforma como Infura en el caso de ethereum, en caso de Tron el proveedor debe ser trongrid.io (Esto debe ser 
    llamado siempre antes que cualquier otro comando en cualquier blockchain, le dice al script a donde dirigir las 
    operaciones...).
Argumentos:
    url: direccion http(s) del nodo.
Errores:
    Codigo de error: 62
Retorna:
    Dict: Key + Boolean
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    set-account: Establece una cuenta o wallet para trabajo posterior sobre ella.
Argumentos:
    with: Llave privada de la cuenta.
Errores:
    Codigo de error: 60
Retorna:
    Dict: Key + String(Name)
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-fee: Obtiene el fee estimado para una transaccion.
Argumentos:
    use: Cantidad de gas usado en la transaccion.
Errores:
    Codigo de error: 54
Retorna:
    Dict: Key + Float
    """
tether_doc = """Entorno Tether(Beta Advertencia: Aun sin probar ciertas opciones, leer primero):
Nota 1: No usar la opcion set-token-type type usdt-erc20 (Si lo usas es bajo su propia responsabilidad)...
Nota 2: usdt-trc20 esta parcialmente probado solo falta probar el deploy del contrato en la mainnet
Acciones:
    transfer: Transfiere una cantidad X de tether hacia una direccion X, notese que aca la llave privada no es solicitada
        lo cual se debe a que es necesario primero una cuenta iniciada en la blockchain. Para esto ver set-provider o 
        set-token-type
Argumentos:
    to: Direccion de destino la cual recibira los tether que le envies. Valor esperado String.
    amount: Cantidad de tether a ser enviado. Valor esperado Float.
Errores: 
    Codigo de error: 40
Retorna:
    Dict: Key + String(hash o transaction id)
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-balance: Obtiene el balance de una cuenta
Argumentos:
    of: direccion de la cual se quiere obtener el balance (Required)
Errores:
    Codigo de error: 50
Retorna:
    Dict: Key + float(balance)	
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    create-account: Crea una cuenta o wallet (Wallet es solo para el caso de bitcoin tanto eth como tron cuentas)
Argumentos:
    with: Private Key to sign the contract transaction into your account. (Blockchain currency is needed)
    parent: Only needed for tron blockchain. Default black hole address  
Errores:
    Codigo de error: 70
Retorna:
    Dict: Key + String(Address), Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-raw-prik: Obtiene la llave privada de la cuenta actual como una cadena formateada...
Argumentos:
    -
Errores:
    Codigo de error: 52
Retorna:
    Dict: Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-prik: Obtiene la llave privada de la cuenta actual en hexadecimal string.
Argumentos:
    -
Errores:
    Codigo de error: 51
Retorna:
    Dict: Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-address: Obtiene la direccion de la cuenta actual.
Argumentos:
    -
Errores:
    Codigo de error: 53
Retorna:
    Dict: Key + Dict(UTxOs)
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-tx-status: Obtiene el estado actual de una transaccion.
Argumentos:
    of: Transaction Id o Hash de la transaccion. Valor esperado, String
Errores:
    Codigo de error: 56
Retorna:
    Dict: Key + Dict(Transaction Details)

--------------------------------------------------------------------------------------------------------------------------
Acciones:
    create-wallet: Crea una cuenta. 
Argumentos:
    -
Errores:
    Codigo de error: 70
Retorna:
    Dict: Key + String(Address), Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    set-provider: Establece un proveedor para las operaciones posteriores con la blockchain, esto puede ser un nodo,
    o una plataforma como Infura o Trongrid.io.
Argumentos:
    url: direccion http(s) del nodo.
Errores:
    Codigo de error: 62
Retorna:
    Dict: Key + Boolean
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    set-account: Establece una cuenta o wallet para trabajo posterior sobre ella.
Argumentos:
    with: Llave privada de la cuenta.
Errores:
    Codigo de error: 60
Retorna:
    Dict: Key + String(Name)
---------------------------------------------------------------------------------------------------------------------------
"""
tron_doc = \
    """Entorno Tron:
Acciones:
    transfer: Transfiere una cantidad X de tron hacia una direccion X
Argumentos:
    to: Direccion de destino la cual recibira los tron que le envies. Valor esperado String.
    amount: Cantidad de tron a ser enviado. Valor esperado Float.
    gas-price: Impuesto a ser pagado a los mineros x cada byte consumido en la operacion. Valor esperado Float. 
    gas-limit: Maximo dispuesto a pagar por la transaccion.
    from: Direccion origen de la transaccion.
    with: Llave privada para firmar la transaccion.
Errores: 
    Codigo de error: 40
Retorna:
    Dict: Key + String(hash o transaction id)
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-balance: Obtiene el balance de una cuenta
Argumentos:
    of: direccion de la cual se quiere obtener el balance (Opcional)
Errores:
    Codigo de error: 50
Retorna:
    Dict: Key + float(balance)	
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    create-account: Crea una cuenta o wallet 
Argumentos:
    -
Errores:
    Codigo de error: 70
Retorna:
    Dict: Key + String(Address), Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-raw-prik: Obtiene la llave privada de la cuenta actual como una cadena formateada...
Argumentos:
    -
Errores:
    Codigo de error: 52
Retorna:
    Dict: Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-prik: Obtiene la llave privada de la cuenta actual en hexadecimal string.
Argumentos:
    -
Errores:
    Codigo de error: 51
Retorna:
    Dict: Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-address: Obtiene la direccion de la cuenta actual.
Argumentos:
    -
Errores:
    Codigo de error: 53
Retorna:
    Dict: Key + Dict(UTxOs)
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    get-tx-status: Obtiene el estado actual de una transaccion.
Argumentos:
    of: Transaction Id o Hash de la transaccion. Valor esperado, String
Errores:
    Codigo de error: 56
Retorna:
    Dict: Key + Dict(Transaction Details)

--------------------------------------------------------------------------------------------------------------------------
Acciones:
    create-wallet: Crea una cuenta. 
Argumentos:
    -
Errores:
    Codigo de error: 70
Retorna:
    Dict: Key + String(Address), Key + String(Private Key)
--------------------------------------------------------------------------------------------------------------------------
Acciones:
    set-provider: Establece un proveedor para las operaciones posteriores con la blockchain, esto puede ser un nodo,
    o una plataforma como Infura en el caso de ethereum, en caso de Tron el proveedor debe ser trongrid.io (Esto debe ser 
    llamado siempre antes que cualquier otro comando en cualquier blockchain, le dice al script a donde dirigir las 
    operaciones...).
Argumentos:
    url: direccion http(s) del nodo.
Errores:
    Codigo de error: 62
Retorna:
    Dict: Key + Boolean
---------------------------------------------------------------------------------------------------------------------------
Acciones:
    set-account: Establece una cuenta o wallet para trabajo posterior sobre ella.
Argumentos:
    with: Llave privada de la cuenta.
Errores:
    Codigo de error: 60
Retorna:
    Dict: Key + String(Name)
---------------------------------------------------------------------------------------------------------------------------
    """