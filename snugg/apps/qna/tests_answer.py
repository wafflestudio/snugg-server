from factory.django import DjangoModelFactory
import factory

class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer

    # TODO: comments
    post = factory.SubFactory(PostFactory)
    writer = factory.SubFactory(UserFactory)
    content = factory.Faker("text")

class AnswerAPITestCase(APITestCase):
    """
    Answer CRUD API request methods included.
    """

    def create_answer(self, data):
        return self.client.post(reverse("answer-list"), data=data)

    def retrieve_answer(self, pk):
        return self.client.get(reverse("answer-detail", args=[pk]))

    def list_answer(self, **params):
        return self.client.get(f"{reverse('answer-list')}?{urlencode(params)}")

    def update_answer(self, pk, data):
        return self.client.put(reverse("answer-detail", args=[pk]), data)

    def partial_update_answer(self, pk, data):
        return self.client.patch(reverse("answer-detail", args=[pk]), data)

    def destroy_answer(self, pk):
        return self.client.delete(reverse("answer-detail", args=[pk]))
