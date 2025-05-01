class RemoveDescriptionFromGyms < ActiveRecord::Migration[8.0]
  def change
    remove_column :gyms, :description, :text
  end
end
