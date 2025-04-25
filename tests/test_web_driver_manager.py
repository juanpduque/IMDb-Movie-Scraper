import pytest
from unittest.mock import MagicMock, patch
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from src.scrapers.utils.web_driver_manager import WebDriverManager


@pytest.fixture
def web_driver_manager():
    """Fixture para WebDriverManager."""
    return WebDriverManager()


def test_init():
    """Test del constructor."""
    manager = WebDriverManager()
    assert manager.driver is None


@patch('src.web_driver_manager.webdriver.Chrome')
@patch('src.web_driver_manager.ChromeDriverManager')
def test_setup_driver_headless(
    mock_chrome_manager,
    mock_chrome,
    web_driver_manager
):
    """Test de configuración del driver en modo headless."""
    # Configurar mocks
    mock_chrome_manager.return_value.install.return_value = (
        "path/to/chromedriver"
    )
    mock_driver = MagicMock(spec=WebDriver)
    mock_chrome.return_value = mock_driver
    
    # Ejecutar setup en modo headless
    driver = web_driver_manager.setup_driver(headless=True)
    
    # Verificar que el driver se configuró correctamente
    assert driver == mock_driver
    assert web_driver_manager.driver == mock_driver
    
    # Verificar que se configuraron las opciones headless
    options = mock_chrome.call_args[1]['options']
    assert isinstance(options, Options)
    assert "--headless" in options.arguments
    assert "--disable-gpu" in options.arguments
    assert "--no-sandbox" in options.arguments


@patch('src.web_driver_manager.webdriver.Chrome')
@patch('src.web_driver_manager.ChromeDriverManager')
def test_setup_driver_normal(
    mock_chrome_manager,
    mock_chrome,
    web_driver_manager
):
    """Test de configuración del driver en modo normal."""
    # Configurar mocks
    mock_chrome_manager.return_value.install.return_value = (
        "path/to/chromedriver"
    )
    mock_driver = MagicMock(spec=WebDriver)
    mock_chrome.return_value = mock_driver
    
    # Ejecutar setup en modo normal
    driver = web_driver_manager.setup_driver(headless=False)
    
    # Verificar que el driver se configuró correctamente
    assert driver == mock_driver
    assert web_driver_manager.driver == mock_driver
    
    # Verificar que no se configuraron opciones headless
    options = mock_chrome.call_args[1]['options']
    assert isinstance(options, Options)
    assert "--headless" not in options.arguments


@patch('src.web_driver_manager.webdriver.Chrome')
@patch('src.web_driver_manager.ChromeDriverManager')
def test_setup_driver_error(
    mock_chrome_manager,
    mock_chrome,
    web_driver_manager
):
    """Test del manejo de errores en la configuración del driver."""
    # Simular error en la inicialización
    mock_chrome.side_effect = Exception("Chrome driver error")
    
    # Verificar que se propaga la excepción
    with pytest.raises(Exception) as exc_info:
        web_driver_manager.setup_driver()
    assert str(exc_info.value) == "Chrome driver error"


def test_quit_driver(web_driver_manager):
    """Test del cierre del driver."""
    # Crear un mock del driver
    mock_driver = MagicMock(spec=WebDriver)
    web_driver_manager.driver = mock_driver
    
    # Ejecutar quit
    web_driver_manager.quit_driver()
    
    # Verificar que se llamó quit y se limpió la referencia
    mock_driver.quit.assert_called_once()
    assert web_driver_manager.driver is None


def test_quit_driver_no_driver(web_driver_manager):
    """Test del cierre cuando no hay driver activo."""
    # Verificar que no hay error al cerrar sin driver
    web_driver_manager.quit_driver()
    assert web_driver_manager.driver is None 