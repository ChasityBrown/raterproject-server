"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterprojectapi.models import Review, Player


class ReviewView(ViewSet):
    """Level up  types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single  review
        
        Returns:
            Response -- JSON serialized  review
        """
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
    


    def list(self, request):
        """Handle GET requests to get all  reviews

        Returns:
            Response -- JSON serialized list of  reviews
        """
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized review instance
        """
        player = Player.objects.get(user=request.auth.user)
        try:
            serializer = CreateReviewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            review = serializer.save(player=player)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for  reviews
    """
    class Meta:
        model = Review
        fields = ('id', 'game', 'review', 'rating')

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'game', 'review', 'rating']