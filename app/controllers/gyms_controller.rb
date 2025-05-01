class GymsController < ApplicationController
  before_action :set_gym, only: %i[ show ]

  # GET /gyms
  def index
    @gyms = Gym.all

    render json: @gyms
  end

  # GET /gyms/1
  def show
    render json: @gym
  end


  # GET /gyms/random
  def random
    gym = Gym.order("RANDOM()").first
    render json: gym
  end

# GET /gyms/search?feature=bouldering
  def search
    if params[:feature].present?
      feature = params[:feature]
      gyms = Gym.where("LOWER(features) LIKE ?", "%#{feature.downcase}%")
      render json: gyms
    else
      render json: { error: "Feature parameter is required" }, status: :bad_request
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_gym
      @gym = Gym.find(params[:id])
    end
    
    def gym_params
      params.require(:gym).permit(:title, :address, :opening_hours, :contact_number, :features)
    end
end
