from qgis.PyQt.QtWidgets import QMessageBox

class MessageBoxHelper():
    def show_not_stated_ip_message_box(self):
        msgbox_not_stated_ip = QMessageBox(QMessageBox.Information, "Ошибка",
                                           "В настройках не указан адрес сервера администрирования.", QMessageBox.Ok)
        msgbox_not_stated_ip.exec()

    def show_getting_projects_error_message_box(self):
        msgbox_getting_projects_error = QMessageBox(QMessageBox.Information, "Ошибка",
                                                    "Ошибка получения списка проектов. Обратитесь к администратору.",
                                                    QMessageBox.Ok)
        msgbox_getting_projects_error.exec()

    def show_empty_administration_server_message_box(self):
        msgbox_empty_administration_server = QMessageBox(QMessageBox.Information, "Ошибка",
                                           'Поле "Сервер администрирования" обязательно к заполнению', QMessageBox.Ok)
        msgbox_empty_administration_server.exec()

    def showProjectOpeningErrorMessageBox(self):
        msgboxProjectOpeningError = QMessageBox(QMessageBox.Information, "Ошибка",
                                                    "Ошибка открытия проекта.\nВозможно у Вас недостаточно прав, обратитесь к администратору.",
                                                    QMessageBox.Ok)
        msgboxProjectOpeningError.exec()

    def showChoosenElementsLayerIsDifferentMessageBox(self):
        msgboxChoosenElementsLayerIsDifferentError = QMessageBox(QMessageBox.Information, "Ошибка",
                                                    "Выбранный элемент находится на другом слое.",
                                                    QMessageBox.Ok)
        msgboxChoosenElementsLayerIsDifferentError.exec()

    def showChoosenElementsEndsDontMatchMessageBox(self):
        msgboxChoosenElementsEndsDontMatchError = QMessageBox(QMessageBox.Information, "Ошибка",
                                                    "Выбранные элементы не имет общих точек на концах.",
                                                    QMessageBox.Ok)
        msgboxChoosenElementsEndsDontMatchError.exec()

    def showChoosenPolygonsDontInstersect(self):
        msgboxChoosenPolygonsDontInstersectError = QMessageBox(QMessageBox.Information, "Ошибка",
                                                    "Выбранные элементы не пересекаются.",
                                                    QMessageBox.Ok)
        msgboxChoosenPolygonsDontInstersectError.exec()

    def showThisTypeOfGeometryIsNotSupported(self):
        msgboxThisTypeOfGeometryIsNotSupportedError = QMessageBox(QMessageBox.Information, "Ошибка",
                                                               "Тип геометрии выбранных элементов не поддерживается.",
                                                               QMessageBox.Ok)
        msgboxThisTypeOfGeometryIsNotSupportedError.exec()
    def showTheSameElementsWereChoosenMessageBox(self):
        msgboxTheSameElementWasChoosenError = QMessageBox(QMessageBox.Information, "Ошибка",
                                                    "Выбранные элементы являеются одним и тем же объектом.",
                                                    QMessageBox.Ok)
        msgboxTheSameElementWasChoosenError.exec()

    def showPathIsAnExistingRegularFileMessageBox(self):
        msgboxPathIsAnExistingRegularFileError = QMessageBox(QMessageBox.Information, "Ошибка",
                                                "Выбранный путь указывает не на DXF-файл.\nВыберите DXF-файл.",
                                                QMessageBox.Ok)
        msgboxPathIsAnExistingRegularFileError.exec()

    def showChoosenDXFisAlreadyInTheList(self):
        msgboxChoosenDXFisAlreadyInTheListError = QMessageBox(QMessageBox.Information, "Ошибка",
                                                             "Вы уже выбрали этот DXF-файл.",
                                                             QMessageBox.Ok)
        msgboxChoosenDXFisAlreadyInTheListError.exec()

    def showGettingGeomertyErrorMessageBox(self):
        msgboxGettingGeomertyError = QMessageBox(QMessageBox.Information, "Ошибка",
                                                             "Ошибка получения списка геометрии.",
                                                             QMessageBox.Ok)
        msgboxGettingGeomertyError.exec()

    def showLayerDoesntExistMessageBox(self):
        msgboxLayerDoesntExistError = QMessageBox(QMessageBox.Information, "Ошибка",
                                                      "Слой не существует.",
                                                      QMessageBox.Ok)
        msgboxLayerDoesntExistError.exec()

    def showProjectIsNotOpenedMessageBox(self):
        msgboxProjectIsNotOpenedError = QMessageBox(QMessageBox.Information, "Ошибка",
                                                  "В данный момент нет открытого проекта.",
                                                  QMessageBox.Ok)
        msgboxProjectIsNotOpenedError.exec()

    def showSomeFilesAreTooBigMessageBox(self):
        msgboxSomeFilesAreTooBigError = QMessageBox(QMessageBox.Information, "Информация!",
                                                  "Некоторые файлы не добавлены, т.к. файлы более 30 МБ добавлять запрещено!",
                                                  QMessageBox.Ok)
        msgboxSomeFilesAreTooBigError.exec()

    def showLoadingAdditionalFilesMessageBox(self):
        msgboxLoadingAdditionalFilesError = QMessageBox(QMessageBox.Information, "Внимание!",
                                                  "Импорт прерван, ошибка загрузки дополнительных файлов на папку файлового хранилища!",
                                                  QMessageBox.Ok)
        msgboxLoadingAdditionalFilesError.exec()

    def showDXFImportToolMessageBox(self):
        msgboxDXFImportToolError = QMessageBox(QMessageBox.Information, "Ошибка",
                                                  "Ошибка запуска инструмента импорта.",
                                                  QMessageBox.Ok)
        msgboxDXFImportToolError.exec()

    def showDrawnLineDoesntIntersectPolygonMessageBox(self):
        msgboxDrawnLineDoesntIntersectPolygon = QMessageBox(QMessageBox.Information, "Ошибка",
                                                  "Нарисованная линия не пересекает полигон",
                                                  QMessageBox.Ok)
        msgboxDrawnLineDoesntIntersectPolygon.exec()


    def showThereAreManyPolylinesMessageBox(self):
        msgboxThereAreManyPolylinesError = QMessageBox(QMessageBox.Information, "Ошибка", "В указанном месте найдено несколько линий.", QMessageBox.Ok)
        msgboxThereAreManyPolylinesError.exec()