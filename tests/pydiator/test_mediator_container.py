from app.pydiator.interfaces import BasePipeline, BaseRequest, BaseNotification, BaseNotificationHandler, BaseResponse, \
    BaseHandler
from app.pydiator.mediatr_container import MediatrContainer
from tests.base_test_case import BaseTestCase


class TestMediatrContainer(BaseTestCase):
    def setUp(self):
        pass

    def test_read_default_values_when_create_instance(self):
        # Given

        # When
        container = MediatrContainer()

        # Then
        assert container.get_requests() == {}
        assert container.get_notifications() == {}
        assert container.get_pipelines() == []

    def test_register_pipeline_when_added_pipeline(self):
        # Given
        class TestPipeline(BasePipeline):
            async def handle(self, req: BaseRequest) -> object:
                pass

        # When
        container = MediatrContainer()
        container.register_pipeline(TestPipeline())

        # Then
        assert container.get_requests() == {}
        assert container.get_notifications() == {}
        assert len(container.get_pipelines()) == 1

    def test_get_pipelines(self):
        # Given
        class TestPipeline(BasePipeline):
            async def handle(self, req: BaseRequest) -> object:
                pass

        # When
        container = MediatrContainer()
        pipeline = TestPipeline()
        container.register_pipeline(pipeline)
        response = container.get_pipelines()

        # Then
        assert container.get_requests() == {}
        assert container.get_notifications() == {}
        assert len(response) == 1
        assert response[0] is pipeline

    def test_register_notification_when_added_notification(self):
        # Given
        class TestNotification(BaseNotification):
            pass

        class TestNotificationHandler(BaseNotificationHandler):

            async def handle(self, notification: BaseNotification):
                pass

        # When
        container = MediatrContainer()
        container.register_notification(TestNotification(), [TestNotificationHandler()])

        # Then
        assert container.get_requests() == {}
        assert container.get_pipelines() == []
        assert len(container.get_notifications()) == 1

    def test_get_notifications(self):
        # Given
        class TestNotification(BaseNotification):
            pass

        class TestNotificationHandler(BaseNotificationHandler):

            async def handle(self, notification: BaseNotification):
                pass

        # When
        container = MediatrContainer()
        notification = TestNotification()
        handlers = [TestNotificationHandler()]
        container.register_notification(notification, handlers)
        response = container.get_notifications()

        # Then
        assert container.get_requests() == {}
        assert container.get_pipelines() == []
        assert len(response) == 1
        assert response[type(notification).__name__] is not None
        assert response[type(notification).__name__] == handlers

    def test_register_request(self):
        # Given
        class TestRequest(BaseRequest):
            pass

        class TestResponse(BaseResponse):
            pass

        class TestHandler(BaseHandler):
            async def handle(self, req: BaseRequest):
                return TestResponse()

        request = TestRequest()
        handler = TestHandler()

        # When
        container = MediatrContainer()
        container.register_request(req=request, handler=handler)

        # Then
        assert container.get_notifications() == {}
        assert len(container.get_requests()) == 1
        assert container.get_requests()[type(request).__name__] is not None
        assert container.get_requests()[type(request).__name__] == handler

    def test_register_request_return_when_request_is_not_instance_of_base_request(self):
        # Given
        class TestRequest(BaseRequest):
            pass

        class TestResponse(BaseResponse):
            pass

        class TestHandler(BaseHandler):
            async def handle(self, req: BaseRequest):
                return TestResponse()

        request = TestRequest()
        handler = TestHandler()

        # When
        container = MediatrContainer()
        container.register_request(req=TestResponse(), handler=handler)

        # Then
        assert len(container.get_requests()) == 0

    def test_register_request_return_when_handler_is_not_instance_of_base_handler(self):
        # Given
        class TestRequest(BaseRequest):
            pass

        class TestResponse(BaseResponse):
            pass

        request = TestRequest()

        # When
        container = MediatrContainer()
        container.register_request(req=request, handler=TestResponse())

        # Then
        assert len(container.get_requests()) == 0
