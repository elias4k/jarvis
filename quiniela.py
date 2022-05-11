from selenium import webdriver


def browser():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        web_driver = webdriver.Chrome('chromedriver.exe', options=options)
    except:
        try:
            print("Error al abrir Chrome")
            web_driver = webdriver.Edge()
        except:
            print("Error al abrir Edge")
            print("Abriendo con Firefox")
            web_driver = webdriver.Firefox()
    return web_driver


def resultados():
    driver = browser()
    driver.get('https://cnq.lotemovil.com.ar/')
    turno = driver.find_element_by_xpath('//*[@id="quiniela-ext-1"]/div/div/div/div[1]/div/div[2]/div[1]/div/span').text
    fecha = driver.find_element_by_xpath('//*[@id="quiniela-ext-1"]/div/div/div/div[1]/div/div[2]/div[3]/div/span').text
    hora = driver.find_element_by_xpath('//*[@id="quiniela-ext-1"]/div/div/div/div[1]/div/div[2]/div[5]/div/span').text
    correntina = driver.find_element_by_xpath('//*[@id="quiniela-ext-1-3"]/div[3]/div[2]/span').text
    la_ciudad = driver.find_element_by_xpath('//*[@id="quiniela-ext-1-1"]/div[3]/div[2]/span').text
    la_provincia = driver.find_element_by_xpath('//*[@id="quiniela-ext-1-2"]/div[3]/div[2]/span').text
    santa_fe = driver.find_element_by_xpath('//*[@id="quiniela-ext-1-4"]/div[3]/div[2]/span').text
    cordoba = driver.find_element_by_xpath('//*[@id="quiniela-ext-1-8"]/div[3]/div[2]/span').text
    entre_rios = driver.find_element_by_xpath('//*[@id="quiniela-ext-1-9"]/div[3]/div[2]/span').text
    return {
        "turno: ": turno,
        "fecha: ": fecha,
        "hora: ": hora,
        "data": {
            "Quiniela Correntina: ": str(correntina),
            "Loteria de la Ciudad: ": str(la_ciudad),
            "Loteria de la provincia: ": str(la_provincia),
            "Loteria de Santa Fe": str(santa_fe),
            "Loteria de Cordoba": str(cordoba),
            "Loteria de Cordoba: ": str(entre_rios)
        }
    }

    driver.quit()
